# Zwift Training Dashboard

[See dashboard](https://google.com)

![Dashboard Screenshot](.github/images/zwift_screenshot.png)

Zwift is a indoor cycling platform that allows you to ride with cyclists from around the world. At the end of each ride, a ".FIT" file that contain details about the training session is generated. I have built an ELT data pipeline that parses the .FIT file, load it into Big Query, transform the data with DBT and visualize it with the Streamlit Python library.

The project showcases:
- ELT pipeline development (Python)
- Cloud data storage (Google Cloud Platform, BigQuery)
- Data transformation and modeling (DBT)
- Data visualization (Plotly) & interactive dashboard development (Streamlit)

## Pipeline Details
1. **Extracting**: Zwift generates FIT files locally, which are automatically backed up to Google Drive on a weekly schedule.
2. **Loading**: FIT files are parsed to extract relevant fields and loaded into BigQuery, with automatic validation to prevent duplicate uploads and remove empty or corrupted files.
3. **Transforming**: The raw data is transformed using DBT.
4. **Visualization**: The data is visualized with Streamlit and Plotly.

## Dependencies
- **fitparse**: FIT file parsing and data extraction
- **Polars**: Primary DataFrame library for efficient data processing
- **pandas-gbq**: Additional BigQuery functionality
- **google-cloud-bigquery**: BigQuery integration
- **pytest**: Testing framework
- **dbt-core**: Data transformation and modeling framework
- **plotly**: Interactive data visualization library
- **Streamlit**: Web application framework for data dashboards

## Error Handling
The pipeline includes robust error handling for:
- Corrupted FIT files (automatically deleted)
- Empty FIT files (automatically deleted)
- BigQuery connection issues
- Missing authentication credentials