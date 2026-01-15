from datetime import datetime, timedelta

# Ignore unresolved dependencies since this file is executed by Airflow, not the local environment.
from airflow import DAG  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore

# Default arguments
default_args = {
    "owner": "sam",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "zwift_etl_daily",
    default_args=default_args,
    description="Daily Zwift data ETL pipeline",
    schedule="0 17 * * *",  # 5pm daily (17:00 in 24-hour format)
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["zwift", "etl"],
) as dag:

    # Task 1: Move Zwift files
    move_files = BashOperator(
        task_id="move_zwift_files",
        bash_command="cd /mnt/c/projects/zwift && poetry run python src/move_zwift_files.py",
    )

    # Task 2: Process FIT files
    process_fit = BashOperator(
        task_id="process_fit_files",
        bash_command="cd /mnt/c/projects/zwift && poetry run python src/fitfile_etl.py",
    )

    # Task 3: Run DBT
    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /mnt/c/projects/zwift && poetry run dbt run",
    )

    # Define task dependencies
    move_files >> process_fit >> run_dbt
