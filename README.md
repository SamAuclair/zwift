# Zwift Training Dashboard

[Link to Zwift Dashboard](https://zwift-dashboard.streamlit.app/)

---

Zwift is an indoor cycling platform that allows you to ride with cyclists from around the world. At the end of each ride, a ".FIT" file that contains details about the training session is generated. I have built an ELT data pipeline that parses the .FIT file, loads it into Big Query, transforms the data with DBT and visualizes it with the Streamlit Python library. The pipeline is orchestrated and scheduled using Apache Airflow.

![Dashboard Screenshot](.github/images/zwift_screenshot.png)

The project showcases:
- Workflow orchestration and scheduling (Apache Airflow)
- ELT pipeline development (Python)
- Cloud data storage (Google Cloud Platform, BigQuery)
- Data transformation and modeling (DBT)
- Data visualization (Plotly) & interactive dashboard development (Streamlit)

## Pipeline Details
1. **Orchestration**: Apache Airflow schedules and manages the daily execution of the ELT pipeline, running at 5pm daily to process new training data.
2. **Extracting**: Zwift generates FIT files locally, which are backed up to Google Drive using an automated script.
3. **Loading**: FIT files are parsed to extract relevant fields and loaded into BigQuery, with automatic validation to prevent duplicate uploads and remove empty or corrupted files.
4. **Transforming**: The raw data is transformed using DBT.
5. **Visualization**: The data is visualized with Streamlit and Plotly.

## Main Dependencies
- **apache-airflow**: Workflow orchestration and scheduling platform
- **pytest**: Testing framework
- **fitparse**: FIT file parsing and data extraction
- **polars**: Primary DataFrame library for efficient data processing
- **google-cloud-bigquery**: BigQuery integration
- **dbt-core**: Data transformation and modeling framework
- **plotly**: Interactive data visualization library
- **streamlit**: Web application framework for data dashboards

## Error Handling
The pipeline includes robust error handling for:
- Corrupted FIT files (automatically deleted)
- Empty FIT files (automatically deleted)
- BigQuery connection issues
- Missing authentication credentials