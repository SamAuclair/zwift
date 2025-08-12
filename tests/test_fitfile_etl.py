import os
from unittest.mock import MagicMock

import pandas as pd
import polars as pl
import pytest

from src.fitfile_etl import (
    clean_fitfile,
    get_existing_filenames_from_bigquery,
    parse_fitfile,
    upload_to_bigquery,
)


def test_parse_fitfile():
    test_fitfile_path = os.path.join(os.path.dirname(__file__), "2023-04-04-12-33-06.fit")
    df = parse_fitfile(test_fitfile_path)

    assert isinstance(df, pl.DataFrame)
    assert any(col in df.columns for col in ["timestamp", "heart_rate", "power", "cadence"])
    assert df.height > 0


def test_clean_fitfile():
    test_fitfile_path = os.path.join(os.path.dirname(__file__), "2023-04-04-12-33-06.fit")
    test_filename = "2023-04-04-12-33-06.fit"
    df = parse_fitfile(test_fitfile_path)
    cleaned_df = clean_fitfile(df, test_filename)

    assert cleaned_df.columns == [
        "file_name",
        "timestamp",
        "heart_rate",
        "power",
        "cadence",
        "speed",
        "enhanced_speed",
    ]
    assert cleaned_df.height > 0


def test_get_existing_filenames_from_bigquery():
    # Mock BigQuery client and query result
    mock_client = MagicMock()
    mock_client.project = "test_project"

    # Create mock rows representing BigQuery results
    mock_row1 = MagicMock()
    mock_row1.file_name = "2023-04-04-12-33-06.fit"
    mock_row2 = MagicMock()
    mock_row2.file_name = "2023-04-05-14-20-15.fit"
    mock_row3 = MagicMock()
    mock_row3.file_name = "2023-04-06-16-45-30.fit"

    # Mock query result
    mock_result = [mock_row1, mock_row2, mock_row3]
    mock_client.query.return_value = mock_result

    # Call the function
    existing_files = get_existing_filenames_from_bigquery(mock_client, "test_dataset", "test_table")

    # Assertions
    expected_query = """
    SELECT DISTINCT file_name
    FROM `test_project.test_dataset.test_table`
    WHERE file_name IS NOT NULL
    """
    mock_client.query.assert_called_once_with(expected_query)

    # Check that the function returns a set with correct filenames
    expected_files = {"2023-04-04-12-33-06.fit", "2023-04-05-14-20-15.fit", "2023-04-06-16-45-30.fit"}
    assert existing_files == expected_files
    assert isinstance(existing_files, set)


def test_upload_to_bigquery_calls_load_table_from_dataframe():
    # Create a dummy DataFrame
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    # Mock BigQuery client and job
    mock_client = MagicMock()
    mock_client.project = "test_project"
    mock_job = MagicMock()
    mock_job.output_rows = 2
    mock_job.result.return_value = None
    mock_client.load_table_from_dataframe.return_value = mock_job

    # Call the function
    output_rows, table_id = upload_to_bigquery(df, mock_client, "test_dataset", "test_table")

    # Assertions
    mock_client.load_table_from_dataframe.assert_called_once_with(
        df, "test_project.test_dataset.test_table"
    )
    mock_job.result.assert_called_once()
    assert output_rows == 2
    assert table_id == "test_project.test_dataset.test_table"
