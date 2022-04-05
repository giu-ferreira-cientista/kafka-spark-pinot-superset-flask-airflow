#!/bin/bash

docker-compose up airflow-init 

docker-compose up -d 

docker exec -t manual-pinot-controller bin/pinot-admin.sh AddTable \
    -schemaFile examples/addtable/patient_schema.json \
    -tableConfigFile examples/addtable/patient_realtime_table_config.json \
    -exec

docker exec -t spark bash -c 'chmod -R 777 *'

docker exec -t spark pip install flask flask-cors kafka-python sseclient pyspark nltk pycaret

docker exec -t spark pip install --upgrade pandas==1.3.4

docker exec -t spark python /home/jovyan/work/api/app.py