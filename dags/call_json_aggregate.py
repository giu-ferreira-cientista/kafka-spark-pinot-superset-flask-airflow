"""DAG using the BashOperator"""

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id='call_json_aggregate_dag',
    schedule_interval='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['stacklabs', 'aggregate', 'json'],
) as dag:
    run_this_last = DummyOperator(
        task_id='dummy',
    )

    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id='call_json_aggregate',
        bash_command='curl http://spark:5000/execute-json-aggregate',
    )
    # [END howto_operator_bash]

    run_this >> run_this_last


if __name__ == "__main__":
    dag.cli()
