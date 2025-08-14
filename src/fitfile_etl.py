import glob
import os

import polars as pl
from fitparse import FitFile
from google.cloud import bigquery

ZWIFT_DATA_FOLDER = r"G:\My Drive\projects\zwift\data"


def parse_fitfile(fitfile_path):
    """
    Parse a FIT file and convert it to a Polars DataFrame.

    Args:
        fitfile_path (str): Path to the FIT file to be parsed.

    Returns:
        polars.DataFrame: DataFrame containing all record messages from the FIT file,
                         with each field as a column. Returns empty DataFrame if no records found.
    """
    with open(fitfile_path, "rb") as f:
        fitfile = FitFile(f)
        records = []
        for record in fitfile.get_messages("record"):
            record_data = {}
            for field in record:
                record_data[field.name] = field.value
            records.append(record_data)
    if records:
        df = pl.DataFrame(records)
    else:
        df = pl.DataFrame([])
    return df


def clean_fitfile(df, filename):
    """
    Clean and filter a FIT file DataFrame to include only relevant columns.

    Extracts specific cycling metrics from the parsed FIT file data and adds
    the source filename for tracking purposes.

    Args:
        df (polars.DataFrame): Raw DataFrame containing parsed FIT file data.
        filename (str): Name of the source FIT file to be added as a column.

    Returns:
        polars.DataFrame: Cleaned DataFrame with columns: file_name, timestamp,
                         heart_rate, power, cadence, speed, enhanced_speed.
    """
    desired_cols = ["timestamp", "heart_rate", "power", "cadence", "speed", "enhanced_speed"]
    cleaned_df = df[desired_cols]
    cleaned_df = cleaned_df.with_columns(pl.lit(filename).alias("file_name"))
    cleaned_df = cleaned_df.select(["file_name"] + desired_cols)
    return cleaned_df


def get_existing_filenames_from_bigquery(client, dataset, table):
    """
    Retrieve all existing FIT file names from a BigQuery table.

    Queries the specified BigQuery table to get all distinct file names that
    have already been processed and uploaded, allowing for duplicate detection.

    Args:
        client (google.cloud.bigquery.Client): BigQuery client instance.
        dataset (str): Name of the BigQuery dataset.
        table (str): Name of the BigQuery table.

    Returns:
        set: Set of existing file names found in the BigQuery table.
    """
    query = f"""
    SELECT DISTINCT file_name
    FROM `{client.project}.{dataset}.{table}`
    WHERE file_name IS NOT NULL
    """
    result = client.query(query)
    existing_files = {row.file_name for row in result}
    return existing_files


def get_fitfile_names_from_folder(folder_path):
    """
    Get all FIT file names from a specified folder.

    Searches for all files with .fit extension in the given folder path and
    returns just the filenames (without full paths) as a set.

    Args:
        folder_path (str): Path to the folder containing FIT files.

    Returns:
        set: Set of FIT file names (basenames only, without paths) found in the folder.
    """
    pattern = os.path.join(folder_path, "*.fit")
    fit_files = glob.glob(pattern)
    filenames = {os.path.basename(file) for file in fit_files}
    return filenames


def upload_to_bigquery(df, client, dataset, table):
    """
    Upload a pandas DataFrame to a BigQuery table.

    Loads the provided DataFrame into the specified BigQuery table using
    the BigQuery client's load_table_from_dataframe method.

    Args:
        df (pandas.DataFrame): DataFrame containing the data to upload.
        client (google.cloud.bigquery.Client): BigQuery client instance.
        dataset (str): Name of the BigQuery dataset.
        table (str): Name of the BigQuery table.

    Returns:
        tuple: A tuple containing (number of rows uploaded, full table ID).
    """
    table_id = f"{client.project}.{dataset}.{table}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    return job.output_rows, table_id


if __name__ == "__main__":
    print("Loading Zwift .fit files to BigQuery...")

    client = bigquery.Client.from_service_account_json("zwift-data-loader-key.json")
    BQ_DATASET = "zwift_data"
    BQ_TABLE = "zwift_fitfile_records"

    # Get all FIT files from zwift data folder
    all_fit_files = get_fitfile_names_from_folder(ZWIFT_DATA_FOLDER)
    print(f"Found {len(all_fit_files)} FIT files in Google Drive")

    # Get existing filenames from BigQuery
    try:
        existing_files = get_existing_filenames_from_bigquery(client, BQ_DATASET, BQ_TABLE)
        print(f"Found {len(existing_files)} FIT files in BigQuery database")
    except Exception as e:
        print(f"Could not query existing files (table may not exist): {e}")
        existing_files = set()

    # Find new files to process
    new_files = all_fit_files - existing_files
    print(f"Found {len(new_files)} new file(s) to load")

    if new_files:
        total_rows_uploaded = 0
        for filename in new_files:
            file_path = os.path.join(ZWIFT_DATA_FOLDER, filename)

            try:
                df = parse_fitfile(file_path)
                if len(df) > 0:
                    df = clean_fitfile(df, filename)
                    pandas_df = df.to_pandas()
                    output_rows, table_id = upload_to_bigquery(pandas_df, client, BQ_DATASET, BQ_TABLE)
                    total_rows_uploaded += output_rows
                    print(f"   Processed '{filename}' successfully ({output_rows} rows).")
                else:
                    print(f"Deleting empty file: {filename}.")
                    os.remove(file_path)
            except Exception as e:
                if "CRC Mismatch" in str(e):
                    print(f"Deleting corrupted file: {filename}.")
                    os.remove(file_path)
                else:
                    print(f"Error processing {filename}: {e}")

        print(f"Total: Loaded {total_rows_uploaded} rows from {len(new_files)} files")

print("--------------------------------")
