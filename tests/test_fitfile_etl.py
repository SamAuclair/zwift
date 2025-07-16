import os
from unittest.mock import MagicMock

import pandas as pd
import polars as pl
import pytest

from src.fitfile_etl import clean_fitfile, parse_fitfile, upload_to_bigquery


def test_parse_fitfile():
    test_fitfile_path = os.path.join(os.path.dirname(__file__), "2023-04-04-12-33-06.fit")
    df = parse_fitfile(test_fitfile_path)

    assert isinstance(df, pl.DataFrame)
    assert any(col in df.columns for col in ["timestamp", "heart_rate", "power", "cadence"])
    assert df.height > 0


def test_clean_fitfile():
    test_fitfile_path = os.path.join(os.path.dirname(__file__), "2023-04-04-12-33-06.fit")
    df = parse_fitfile(test_fitfile_path)
    cleaned_df = clean_fitfile(df)

    assert cleaned_df.columns == [
        "timestamp",
        "heart_rate",
        "power",
        "cadence",
        "speed",
        "enhanced_speed",
    ]
    assert cleaned_df.height > 0


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
