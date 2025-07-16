import polars as pl
from fitparse import FitFile
from google.cloud import bigquery

FITFILE_PATH = r"G:\My Drive\projects\health\zwift data\2021-12-30-13-00-11.fit"


def parse_fitfile(fitfile_path):
    fitfile = FitFile(fitfile_path)
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


def clean_fitfile(df):
    desired_cols = ["timestamp", "heart_rate", "power", "cadence", "speed", "enhanced_speed"]
    return df[desired_cols]


def upload_to_bigquery(df, client, dataset, table):
    table_id = f"{client.project}.{dataset}.{table}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    return job.output_rows, table_id


if __name__ == "__main__":
    df = parse_fitfile(FITFILE_PATH)
    df = clean_fitfile(df)
    pandas_df = df.to_pandas()

    client = bigquery.Client.from_service_account_json("zwift-data-loader-key.json")
    BQ_DATASET = "zwift_data"
    BQ_TABLE = "zwift_fitfile_records"

    output_rows, table_id = upload_to_bigquery(pandas_df, client, BQ_DATASET, BQ_TABLE)
    print(f"Loaded {output_rows} rows to {table_id}")
