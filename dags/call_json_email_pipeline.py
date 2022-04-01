"""DAG using the BashOperator"""

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id='call_json_email_pipeline_dag',
    schedule_interval='@weekly',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['stacklabs', 'pipeline', 'email', 'json'],
) as dag:
    # [START email_inference_operator_bash]
    run_json_email_inference = BashOperator(
        task_id='call_json_email_inference',
        bash_command='curl http://spark:5000/execute-json-email-inference',
    )
    # [END operator_bash]

    # [START email_consumer_operator_bash]
    run_json_email_consumer = BashOperator(
        task_id='call_json_email_consumer',
        bash_command='curl http://spark:5000/execute-json-email-consumer',
    )
    # [END operator_bash]


    run_json_email_inference >> run_json_email_consumer


if __name__ == "__main__":
    dag.cli()
