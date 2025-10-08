"""
Zwift ETL DAG

This DAG orchestrates the Zwift data pipeline:
1. Move Zwift FIT files from local folder to Google Drive
2. Process FIT files and upload to BigQuery
3. Run dbt transformations

Schedule: Monday, Thursday and Saturday at 5:00 PM
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Sam",
    "depends_on_past": True,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": "auclair.sam@gmail.com",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 1),
}

dag = DAG(
    "zwift_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for Zwift FIT files to BigQuery",
    schedule_interval="0 17 * * 1,4,6",
    catchup=False,
    tags=["zwift", "etl", "bigquery"],
)

# Task 1: Move Zwift files from local folder to Google Drive
move_files_task = BashOperator(
    task_id="move_zwift_files",
    bash_command="cd C:\\projects\\Zwift && poetry run python src\\move_zwift_files.py",
    dag=dag,
)

# Task 2: Process FIT files and upload to BigQuery
process_fitfiles_task = BashOperator(
    task_id="process_fitfiles",
    bash_command="cd C:\\projects\\Zwift && poetry run python src\\fitfile_etl.py",
    dag=dag,
)

# Task 3: Run dbt transformations
run_dbt_task = BashOperator(
    task_id="run_dbt",
    bash_command="cd C:\\projects\\Zwift && poetry run dbt run",
    dag=dag,
)

# Define task dependencies
move_files_task >> process_fitfiles_task >> run_dbt_task
