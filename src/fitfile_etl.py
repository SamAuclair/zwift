import polars as pl
from fitparse import FitFile

FITFILE_PATH = r"G:\My Drive\projects\health\zwift data\2023-04-04-12-33-06.fit"


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
    desired_cols = ["timestamp", "heart_rate", "power", "cadence"]
    return df[desired_cols]


if __name__ == "__main__":
    df = parse_fitfile(FITFILE_PATH)
    df = clean_fitfile(df)
