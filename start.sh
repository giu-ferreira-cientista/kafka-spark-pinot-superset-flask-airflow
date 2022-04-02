#!/bin/bash

docker-compose up airflow-init 

docker-compose up -d 

docker exec -t manual-pinot-controller bin/pinot-admin.sh AddTable \
    -schemaFile examples/addtable/patient_schema.json \
    -tableConfigFile examples/addtable/patient_realtime_table_config.json \
    -exec
