# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project for processing Zwift FIT files and uploading the data to Google BigQuery. The project uses Poetry for dependency management and includes ETL functionality for cycling data analysis.

## Development Commands

### Environment Setup
```bash
poetry install
```

### Running Tests
```bash
poetry run pytest
```

### Running Individual Test Files
```bash
poetry run pytest tests/test_fitfile_etl.py
```

### Running the Main ETL Script
```bash
poetry run python src/fitfile_etl.py
```

### Running the File Moving Script
```bash
poetry run python src/move_zwift_files.py
# Or use the batch file on Windows:
move_zwift_files.bat
```

## Architecture

### Core Modules

- **`src/fitfile_etl.py`**: Main ETL pipeline for processing FIT files
  - `parse_fitfile()`: Converts FIT files to Polars DataFrames using fitparse library
  - `clean_fitfile()`: Filters DataFrame to relevant columns (timestamp, heart_rate, power, cadence, speed, enhanced_speed)
  - `upload_to_bigquery()`: Uploads processed data to Google BigQuery using service account authentication

- **`src/move_zwift_files.py`**: Utility for moving Zwift activity files from local OneDrive directory to Google Drive storage location

### Data Flow

1. Zwift generates FIT files in `C:\Users\aucla\OneDrive\Documents\Zwift\Activities`
2. `move_zwift_files.py` moves files to `G:\My Drive\projects\health\zwift data`
3. `fitfile_etl.py` processes FIT files and uploads to BigQuery dataset `zwift_data.zwift_fitfile_records`

### Dependencies

- **Polars**: Primary DataFrame library for data processing
- **fitparse**: FIT file parsing
- **google-cloud-bigquery/pandas-gbq**: BigQuery integration
- **pytest**: Testing framework

### Authentication

The project expects a `zwift-data-loader-key.json` file in the root directory for BigQuery authentication using a service account.