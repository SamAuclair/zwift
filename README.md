# Zwift FIT File ETL Pipeline

A Python ETL pipeline for processing Zwift FIT files and uploading cycling data to Google BigQuery for analysis.

The project showcases:
- ETL pipeline development (Python)
- Cloud data storage and processing (Google Cloud Platform, BigQuery)
- Data transformation and modeling (DBT)
- Interactive dashboard development (Streamlit)
- Data visualization (Plotly)

## Overview

This project automates the collection and processing of Zwift cycling activity data by:
- Moving FIT files from local Zwift directory to Google Drive storage
- Parsing FIT files to extract cycling metrics (heart rate, power, cadence, speed)
- Uploading processed data to Google BigQuery for analysis
- Avoiding duplicate uploads by checking existing records

## Prerequisites

- Python 3.8+
- Poetry (for dependency management)
- Google Cloud service account with BigQuery access
- Zwift application generating FIT files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SamAuclair/Zwift.git
cd Zwift
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up Google Cloud authentication:
   - Place your service account key file as `zwift-data-loader-key.json` in the project root
   - Ensure the service account has BigQuery read/write permissions

## Usage

### Process and Upload FIT Files

Run the main ETL pipeline to process all new FIT files:

```bash
poetry run python src/fitfile_etl.py
```

This will:
- Scan the data folder for FIT files
- Check BigQuery for existing records to avoid duplicates
- Process new files and upload to BigQuery
- Remove empty or corrupted files automatically

### Move Files from Local Zwift Directory

Move FIT files from your local Zwift directory to Google Drive:

```bash
poetry run python src/move_zwift_files.py
```

Or use the Windows batch file:
```bash
move_zwift_files.bat
```

## Architecture

### Data Flow

1. **Collection**: Zwift generates FIT files in `C:\Users\<username>\OneDrive\Documents\Zwift\Activities`
2. **Storage**: Files are moved to `G:\My Drive\projects\zwift\data`
3. **Processing**: FIT files are parsed and cleaned to extract relevant metrics
4. **Upload**: Processed data is uploaded to BigQuery dataset `zwift_data.zwift_fitfile_records`

### Core Functions

- `parse_fitfile()`: Converts FIT files to Polars DataFrames using fitparse library
- `clean_fitfile()`: Filters DataFrame to relevant columns (timestamp, heart_rate, power, cadence, speed, enhanced_speed)
- `get_fitfile_names_from_folder()`: Retrieves all FIT file names from specified folder
- `get_existing_filenames_from_bigquery()`: Queries BigQuery for existing records to prevent duplicates
- `upload_to_bigquery()`: Uploads processed data to Google BigQuery

## Data Schema

The processed data includes the following fields:
- `file_name`: Source FIT file name
- `timestamp`: Activity timestamp
- `heart_rate`: Heart rate (BPM)
- `power`: Power output (watts)
- `cadence`: Pedaling cadence (RPM)
- `speed`: Speed (m/s)
- `enhanced_speed`: Enhanced speed measurement (m/s)

## Testing

Run the test suite:
```bash
poetry run pytest
```

Run specific test files:
```bash
poetry run pytest tests/test_fitfile_etl.py
```

## Dependencies

- **Polars**: Primary DataFrame library for efficient data processing
- **fitparse**: FIT file parsing and data extraction
- **google-cloud-bigquery**: BigQuery integration
- **pandas-gbq**: Additional BigQuery functionality
- **pytest**: Testing framework

## Configuration

The pipeline uses these default configurations:
- Local Zwift directory: `C:\Users\<username>\OneDrive\Documents\Zwift\Activities`
- Google Drive storage: `G:\My Drive\projects\zwift\data`
- BigQuery dataset: `zwift_data`
- BigQuery table: `zwift_fitfile_records`

## Error Handling

The pipeline includes robust error handling for:
- Corrupted FIT files (automatically deleted)
- Empty FIT files (automatically deleted)
- BigQuery connection issues
- Missing authentication credentials