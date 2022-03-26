# Data Pipeline API with Flask, Kafka, Spark, Pinot and Superset 
Repositorio para armazenar os artefatos do projeto de conexao da API em Flask com o Kafka, processamento dos dados via spark e posterior OLAP Realtime with Low Latency com o Pinot e e integração do Dashboard com o Superset para exibição dos gráficos.


# USE DOCKER COMPOSE TO LOAD THE ENVIROMENT - kafka, kafka-ui, jupyter, spark, pinot, superset and airflow

$ echo -e "AIRFLOW_UID=$(id -u)" > .env

$ docker-compose up airflow-init

$ docker-compose up -d

# Shell into spark container

$ pip install flask flask-cors kafka-python sseclient

$ chmod -R 777 api csv json notebooks app

$ cd api

$ python app.py

$ curl <ip_spark>:5000/execute-csv

$ curl <ip_spark>:5000/execute-api

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


# Create Pinot Table Schema
$ docker cp pinot/examples/airlineStats_realtime_table_config.json manual-pinot-controller:/opt/pinot/examples/airlineStats_realtime_table_config.json

# Sheel into manual-pinot-controller and Add Table
$ bin/pinot-admin.sh AddTable \
    -schemaFile examples/addtable/patient_schema.json \
    -tableConfigFile examples/addtable/patient_realtime_table_config.json \
    -exec        

$ bin/pinot-admin.sh ChangeTableState -tableName patients -state drop -controllerHost pinot-controller -controllerPort 9000


# Configure Superset Enviroment

# Shell into superset container
$ pip install pinotdb==0.3.9

$ docker cp ./superset/pinot_superset_datasource.yaml superset:/etc/examples/pinot/pinot_superset_datasource.yaml
$ superset import_datasources -p /etc/examples/pinot/pinot_superset_datasource.yaml


# You will Need to Restart superset container and run commands below

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
    bash -c 'superset import_datasources -p /etc/examples/pinot/pinot_example_datasource_quickstart.yaml && \
             superset import_dashboards -p /etc/examples/pinot/pinot_example_dashboard.json'




# Load Sample Data into Kafka Topic and Query Pinot and Superset Again!
{"Quarter":1,"FlightNum":1,"Origin":"JFK","LateAircraftDelay":null,"DivActualElapsedTime":null,"DivWheelsOns":null,"DivWheelsOffs":null,"ArrDel15":0,"AirTime":359,"DivTotalGTimes":null,"DepTimeBlk":"0900-0959","DestCityMarketID":32575,"DaysSinceEpoch":16071,"DivAirportSeqIDs":null,"DepTime":914,"Month":1,"DestStateName":"California","CRSElapsedTime":385,"Carrier":"AA","DestAirportID":12892,"Distance":2475,"ArrTimeBlk":"1200-1259","SecurityDelay":null,"DivArrDelay":null,"LongestAddGTime":null,"OriginWac":22,"WheelsOff":934,"UniqueCarrier":"AA","DestAirportSeqID":1289203,"DivReachedDest":null,"Diverted":0,"ActualElapsedTime":384,"AirlineID":19805,"OriginStateName":"New York","FlightDate":"2014-01-01","DepartureDelayGroups":0,"DivAirportLandings":0,"OriginCityName":"New York, NY","OriginStateFips":36,"OriginState":"NY","DistanceGroup":10,"WeatherDelay":null,"DestWac":91,"WheelsOn":1233,"OriginAirportID":12478,"OriginCityMarketID":31703,"NASDelay":null,"DestState":"CA","ArrTime":1238,"ArrivalDelayGroups":0,"Flights":1,"DayofMonth":1,"RandomAirports":["SEA","PSC","PHX","MSY","ATL","TYS","DEN","CHS","PDX","LAX","EWR","SFO","PIT","RDU","RAP","LSE","SAN","SBN","IAH","OAK","BRO","JFK","SAT","ORD","ACY","DFW","BWI","TPA","BFL","BOS","SNA","ISN"],"TotalAddGTime":null,"CRSDepTime":900,"DayOfWeek":3,"Dest":"LAX","CancellationCode":null,"FirstDepTime":null,"DivTailNums":null,"DepDelayMinutes":14,"DepDelay":14,"TaxiIn":5,"OriginAirportSeqID":1247802,"DestStateFips":6,"ArrDelay":13,"Cancelled":0,"DivAirportIDs":null,"TaxiOut":20,"DepDel15":0,"CarrierDelay":null,"DivLongestGTimes":null,"DivAirports":null,"DivDistance":null,"Year":2014,"CRSArrTime":1225,"ArrDelayMinutes":13,"TailNum":"N338AA","DestCityName":"Los Angeles, CA"}


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