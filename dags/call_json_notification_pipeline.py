"""DAG using the BashOperator"""

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id='call_json_notification_pipeline_dag',
    schedule_interval= '@once',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['stacklabs', 'pipeline', 'notification', 'json'],
) as dag:
    # [START producer_operator_bash]
    run_json_producer = BashOperator(
        task_id='call_json_producer',
        bash_command='curl http://spark:5000/execute-json-producer',
    )
    # [END operator_bash]

    # [START aggregate_operator_bash]
    run_json_aggregate = BashOperator(
        task_id='call_json_aggregate',
        bash_command='curl http://spark:5000/execute-json-aggregate',
    )
    # [END operator_bash]

    # [START notification_inference_operator_bash]
    run_json_notification_inference = BashOperator(
        task_id='call_json_notification_inference',
        bash_command='curl http://spark:5000/execute-json-notification-inference',
    )
    # [END operator_bash]

    # [START notification_consumer_operator_bash]
    run_json_notification_consumer = BashOperator(
        task_id='call_json_notification_consumer',
        bash_command='curl http://spark:5000/execute-json-notification-consumer',
    )
    # [END operator_bash]


    run_json_notification_consumer >> run_json_notification_inference >> run_json_aggregate >> run_json_producer   


if __name__ == "__main__":
    dag.cli()
