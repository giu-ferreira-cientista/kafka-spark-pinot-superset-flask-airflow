# Data Pipeline API with Flask, Kafka, Spark, Pinot and Superset 
Repositorio para armazenar os artefatos do projeto de conexao da API em Flask com o Kafka, processamento dos dados via spark e posterior OLAP Realtime with Low Latency com o Pinot e e integração do Dashboard com o Superset para exibição dos gráficos.


# USE DOCKER COMPOSE TO LOAD THE ENVIROMENT - kafka, kafka-ui, jupyter, spark, pinot, superset and airflow

$ echo -e "AIRFLOW_UID=$(id -u)" > .env

$ docker-compose up airflow-init

$ docker-compose up -d

# Shell into spark container

$ pip install flask flask-cors kafka-python sseclient pyspark

$ chmod -R 777 api csv json notebooks app

$ cd api

$ python app.py

$ python app-ml.py

Start airflow csv_producer and api_producer dags


Main Published Ports:
- 8081 - Kafka-Ui
- 9000 - Pinot
- 8888 - Jupyter / Pyspark Notebook
- 8088 - Superset

Main Services Ports:
- 9092  - Kafka
- 29092 - Kafka Broker
- 2181  - Zookeeper
- 2182  - Pinot Zookeeper
- 9000  - Pinot Controller
- 8099  - Pinot Broker
- 8098  - Pinot Server
- 4040  - Spark
- 5000  - Rest API 


# Shell into manual-pinot-controller and Add Table
$ bin/pinot-admin.sh AddTable \
    -schemaFile examples/addtable/patient_schema.json \
    -tableConfigFile examples/addtable/patient_realtime_table_config.json \
    -exec   
         
# Para apagar (apenas se for necessario)
$ bin/pinot-admin.sh ChangeTableState -tableName patients -state drop -controllerHost pinot-controller -controllerPort 9000


# Configure Superset Enviroment

# Shell into superset container
$ pip install pinotdb==0.3.9

# run commands below in host bash

$ docker exec -it superset superset fab create-admin \
               --username admin \
               --firstname Superset \
               --lastname Admin \
               --email admin@superset.com \
               --password admin

$ docker exec -it superset superset db upgrade

$ docker exec -it superset superset init

$ docker exec \
    -t superset \
    bash -c 'superset import-dashboards -p /superset/dashboard_pinot_superset_add_exercicio.zip'

    Or Login on browser and import dashboard file "/superset/dashboard_pinot_superset_add_exercicio.zip"


# Load Sample Data into Kafka Topic and Query Pinot and Superset Again!
{"id":1,"nome":"joao","idade":34,"sexo":0,"peso":59,"altura":170,"bpm":84,"pressao":125,"respiracao":19,"temperatura":36,"glicemia":121,"saturacao_oxigenio":95,"estado_atividade":1,"dia_de_semana":0,"periodo_do_dia":0,"semana_do_mes":0,"estacao_do_ano":3,"passos":151,"calorias":12.08,"distancia":188.75,"tempo":2.416,"total_sleep_last_24":7,"deep_sleep_last_24":6,"light_sleep_last_24":3,"awake_last_24":16,"fumante":1,"genetica":1,"gestante":0,"frutas":0,"vegetais":0,"alcool":1,"doenca_coracao":1,"avc":1,"colesterol_alto":1, "exercicio":0, "timestampstr":"2022-03-04 11:18:03","timestamp_epoch":"1646392683"}

# Running the Flask API Producers and Consumers

# Create Kafka Topics (Inspect in kafka0 ang get <kafka0> ip address and change in commands below. Shell in kafka-zookeeper and run commands below)

$ kafka-topics --create --bootstrap-server <kafka0>:29092 --replication-factor 1 --partitions 3 --topic INFERENCE

$ kafka-topics --create --bootstrap-server <kafka0>:29092 --replication-factor 1 --partitions 3 --topic EMAIL

$ kafka-topics --create --bootstrap-server <kafka0>:29092 --replication-factor 1 --partitions 3 --topic NOTIFICATION

# Console - Produce some events
$ kafka-console-producer --broker-list <kafka0>:29092 --topic INFERENCE
kafka-console-producer --broker-list 172.18.0.10:29092 --topic INFERENCE

# Console - Open Consumer
$ kafka-console-consumer --bootstrap-server <kafka0>:9092 --topic INFERENCE
kafka-console-consumer --bootstrap-server 172.18.0.10:9092 --topic INFERENCE

# Install Python Packages
$ pip install flask

$ pip install flask-cors

$ pip install kafka-python

# Run API
$ python app.py

# Alternative - install gunicorn
$ #pip install gunicorn
$ #folder where app.py file is 
$ #gunicorn -k gthread -w 2 -t 40000 --threads 3 -b:5000 app:app

# Run Python Consumers
$ python inference_consumer.py

$ python email_consumer.py

$ python notification_consumer.py

# Run Random Producer
$ python random_producer.py

# Run API Producer
$ python REST_API_producer.py

# Run Random API Producer
$ python random_REST_API_producer.py

# Run REST API Consumer
$ python REST_API_consumer.py

# Just Sit and Watch!
$ Check Kafka-Ui and console logs to see the data flow

# Include Spark Structured Streaming Processing
open 8888 port on your browser

# Shell into spark-1 Container
$ jupyter notebook list

copy and paste token on your browser

# Running Spark Apps
open all notebooks in this order and click Cell>Run All: producer, consumer, datavisualization 

# Check Results on Kafka-Ui and Console Logs
Query kafka topics and check the generated graphics and tables


# Include Airlfow
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.4/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
docker-compose up
Open browser port 8080 and login wit user airflow and password airflow

# Copy DAG file to airflow directory
docker cp dags/call_api_producer.py kafka-spark-pinot-superset-flask-airflow-airflow-webserver-1:/home/airflow/.local/lib/python3.7/site-packages/airflow/example_dags/call_api_producer.py

docker cp kafka-spark-pinot-superset-flask-airflow-airflow-webserver-1:/home/airflow/.local/lib/python3.7/site-packages/airflow/example_dags/example_bash_operator.py dags/example_bash_operator.py

# Include Spark API (Shell into Spark Container)
$ pip install flask

$ pip install flask-cors

$ python app.py

Find IP address of spark container to call the API on : <ip_spark>:5000/execute

Or open the url on browser to call the API  : <ip_spark>:5500/execute

# Command to execute via API (shell into spark container to test it)

$ pip install sseclient

$ pip install kafka-python

$ spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5,io.delta:delta-core_2.12:0.7.0 --master local[*] --driver-memory 12g --executor-memory 12g work/notebooks/event-producer.py



# Another example 
$ docker cp pinot/examples/transcript_realtime_table_config.json manual-pinot-controller:/opt/pinot/examples/transcript_realtime_table_config.json

$ docker cp pinot/examples/transcript_schema.json manual-pinot-controller:/opt/pinot/examples/transcript_schema.json

# Shell into Pinot controller 
$ bin/pinot-admin.sh AddTable \
    -schemaFile examples/transcript_schema.json \
    -tableConfigFile examples/transcript_realtime_table_config.json \
    -exec

# Load sample data 
open pinot/examples/transcript_sample_data.json and copy and paste into kafka-ui


# Stop Flask
$ stop the Flask Server with Ctrl-C

# Stop Producers and Consumers
$ stop terminals with Ctrl-C

# Stop Kafka
$ docker-compose docker-compose_kafka_spark_pinot_superset.yaml down

# Stop all containers docker
$ docker kill $(docker ps -q)
$ docker rm $(docker ps -a -q)
$ docker rmi $(docker images -q)

# Clean and Prune Docler Enviroment
$ docker system prune --all --force --volumes