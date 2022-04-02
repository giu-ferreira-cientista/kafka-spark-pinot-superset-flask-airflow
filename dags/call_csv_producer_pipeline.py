"""DAG using the BashOperator"""

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id='call_csv_producer_pipeline_dag',
    schedule_interval='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['stacklabs', 'pipeline', 'producer', 'csv'],
) as dag:
    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id='call_csv_producer',
        bash_command='curl http://spark:5000/execute-csv-producer',
    )
    # [END howto_operator_bash]

    run_this


if __name__ == "__main__":
    dag.cli()
