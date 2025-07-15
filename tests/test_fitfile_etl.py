import os

import polars as pl

from src.fitfile_etl import clean_fitfile, parse_fitfile


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

    assert cleaned_df.columns == ["timestamp", "heart_rate", "power", "cadence"]
    assert cleaned_df.height > 0
