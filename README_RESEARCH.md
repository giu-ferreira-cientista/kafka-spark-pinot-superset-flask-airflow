# Flask and Kafka
Repositorio para armazenar os artefatos do projeto de conexao da API em Flask com o Kafka, processamento dos dados via spark e posterior OLAP Realtime with Low Latency com o Pinot e criação do Dashboard com o Superset para exibição de gráficos

https://kafka.apache.org/quickstart

wget https://www.apache.org/dyn/closer.cgi?path=/kafka/3.1.0/kafka_2.13-3.1.0.tgz

tar -xzf kafka_2.13-3.1.0.tgz

# USE KAFKA COMPOSE WITH UI - load kafka ui and kafka in compose
docker-compose up -d


# OR Start Kafka Manually
cd kafka_2.13-3.1.0

# Start the ZooKeeper service
#Note: Soon, ZooKeeper will no longer be required by Apache Kafka.
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties



# Create Kafka Topics

bin/kafka-topics.sh --create --topic INFERENCE --bootstrap-server localhost:9092
or
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic INFERENCE

bin/kafka-topics.sh --create --topic EMAIL --bootstrap-server localhost:9092

bin/kafka-topics.sh --create --topic NOTIFICATION --bootstrap-server localhost:9092

# Describe topic
bin/kafka-topics.sh --describe --topic INFERENCE --bootstrap-server localhost:9092

# Produce some events
bin/kafka-console-producer.sh --topic INFERENCE --bootstrap-server localhost:9092

# Open Consumer
bin/kafka-console-consumer.sh --topic INFERENCE --from-beginning --bootstrap-server localhost:9092

# Run API
python app.py

# Alternative - install gunicorn
#pip install gunicorn
#folder where app.py file is 
#gunicorn -k gthread -w 2 -t 40000 --threads 3 -b:5000 app:app


# Run Python Consumers
python inference_consumer.py

python email_consumer.py

python notification_consumer.py

# Run Random Producer
python random_producer.py

# Run API Producer
python REST_API_producer.py

# Run Random API Producer
python random_REST_API_producer.py

# Run REST API Consumer
python REST_API_consumer.py

# Improve Infrastructure

# Include Pinot Docker
cd pinot

docker-compose up -d

# Manual Install Pinot

wget https://downloads.apache.org/pinot/apache-pinot-0.9.3/apache-pinot-0.9.3-bin.tar.gz

export PINOT_VERSION=0.9.3

tar -xvf apache-pinot-${PINOT_VERSION}-bin.tar.gz

cd apache-pinot-${PINOT_VERSION}-bin
ls

PINOT_INSTALL_DIR=`pwd`

cd apache-pinot-${PINOT_VERSION}-bin

export _JAVA_OPTIONS=-Xmx8024m 

bin/pinot-admin.sh StartZookeeper

export _JAVA_OPTIONS=-Xmx8024m 

bin/pinot-admin.sh StartController \
    -zkAddress localhost:2181

export _JAVA_OPTIONS=-Xmx8024m 

bin/pinot-admin.sh StartBroker -zkAddress localhost:2181

export _JAVA_OPTIONS=-Xmx8024m 

bin/pinot-admin.sh StartServer -zkAddress localhost:2181        

# Create Pinot table

export _JAVA_OPTIONS=-Xmx8024m 

*arquivo original editado

docker cp pinot/examples/airlineStats_realtime_table_config.json manual-pinot-controller:/opt/pinot/examples/airlineStats_realtime_table_config.json

# Inspect into manual-pinot-controller

bin/pinot-admin.sh AddTable \
    -schemaFile examples/stream/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/airlineStats_realtime_table_config.json \
    -exec    

# Load Data into Kafka Topic and Query Pinot Table Again

# Sample Data 
{"Quarter":1,"FlightNum":1,"Origin":"JFK","LateAircraftDelay":null,"DivActualElapsedTime":null,"DivWheelsOns":null,"DivWheelsOffs":null,"ArrDel15":0,"AirTime":359,"DivTotalGTimes":null,"DepTimeBlk":"0900-0959","DestCityMarketID":32575,"DaysSinceEpoch":16071,"DivAirportSeqIDs":null,"DepTime":914,"Month":1,"DestStateName":"California","CRSElapsedTime":385,"Carrier":"AA","DestAirportID":12892,"Distance":2475,"ArrTimeBlk":"1200-1259","SecurityDelay":null,"DivArrDelay":null,"LongestAddGTime":null,"OriginWac":22,"WheelsOff":934,"UniqueCarrier":"AA","DestAirportSeqID":1289203,"DivReachedDest":null,"Diverted":0,"ActualElapsedTime":384,"AirlineID":19805,"OriginStateName":"New York","FlightDate":"2014-01-01","DepartureDelayGroups":0,"DivAirportLandings":0,"OriginCityName":"New York, NY","OriginStateFips":36,"OriginState":"NY","DistanceGroup":10,"WeatherDelay":null,"DestWac":91,"WheelsOn":1233,"OriginAirportID":12478,"OriginCityMarketID":31703,"NASDelay":null,"DestState":"CA","ArrTime":1238,"ArrivalDelayGroups":0,"Flights":1,"DayofMonth":1,"RandomAirports":["SEA","PSC","PHX","MSY","ATL","TYS","DEN","CHS","PDX","LAX","EWR","SFO","PIT","RDU","RAP","LSE","SAN","SBN","IAH","OAK","BRO","JFK","SAT","ORD","ACY","DFW","BWI","TPA","BFL","BOS","SNA","ISN"],"TotalAddGTime":null,"CRSDepTime":900,"DayOfWeek":3,"Dest":"LAX","CancellationCode":null,"FirstDepTime":null,"DivTailNums":null,"DepDelayMinutes":14,"DepDelay":14,"TaxiIn":5,"OriginAirportSeqID":1247802,"DestStateFips":6,"ArrDelay":13,"Cancelled":0,"DivAirportIDs":null,"TaxiOut":20,"DepDel15":0,"CarrierDelay":null,"DivLongestGTimes":null,"DivAirports":null,"DivDistance":null,"Year":2014,"CRSArrTime":1225,"ArrDelayMinutes":13,"TailNum":"N338AA","DestCityName":"Los Angeles, CA"}

# Drop Table Pinot
bin/pinot-admin.sh ChangeTableState -tableName airlineStats_REALTIME -state drop -controllerHost 172.18.0.4 -controllerPort 9000 -exec

# Or load avro
bin/pinot-admin.sh StreamAvroIntoKafka \
  -avroFile examples/stream/airlineStats/sample_data/airlineStats_data.avro \
  -kafkaTopic flights-realtime -kafkaBrokerList localhost:9092 -zkAddress localhost:2181/kafka

# Include Presto
docker run --name=presto-coordinator \
  -p 8880:8080 \
  -d apachepinot/pinot-presto:latest

# Include Superset
git clone https://github.com/apache/superset.git

cd superset

docker-compose -f docker-compose-non-dev.yml pull
docker-compose -f docker-compose-non-dev.yml up

# Or Docker Run Superset 

docker run -d -p 8080:8088 --name superset apache/superset

docker exec -it superset superset fab create-admin \
               --username admin \
               --firstname Superset \
               --lastname Admin \
               --email admin@superset.com \
               --password admin

docker exec -it superset superset db upgrade

docker exec -it superset superset load_examples

docker exec -it superset superset init

Login and take a look -- navigate to http://localhost:8080/login/ -- u/p: [admin/admin]
:

# Install Superset Database Driver

touch ./docker/requirements-local.txt

echo "pinotdb" >> ./docker/requirements-local.txt

docker-compose build --force-rm

docker-compose up

# Inspect pinot containers to get ips 
pinot+http://<ip_pinot_broker>:8099/query?server=http://<ip_pinot_controller>:9000/

pinot+http://172.29.0.12:8099/query?server=http://172.29.0.8:9000/

# Superset Pinot Version
docker run --name=superset \
  -p 8088:8088 \
  -d apachepinot/pinot-superset:latest

docker exec -it superset superset fab create-admin \
               --username admin \
               --firstname Superset \
               --lastname Admin \
               --email admin@superset.com \
               --password admin

docker exec -it superset superset db upgrade

docker exec -it superset superset init

docker exec \
    -t superset \
    bash -c 'superset import_datasources -p /etc/examples/pinot/pinot_example_datasource_quickstart.yaml && \
             superset import_dashboards -p /etc/examples/pinot/pinot_example_dashboard.json'


pinot+http://172.29.0.12:8099/query?server=http://172.29.0.8:9000/

# Include Airflow
cd airflow

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.4/docker-compose.yaml'

mkdir -p ./dags ./logs ./plugins

echo -e "AIRFLOW_UID=$(id -u)" > .env

docker-compose up airflow-init

docker-compose up

localhost:8080

# Include Trino
git clone https://github.com/bitsondatadev/trino-getting-started.git

cd trino-getting-started

cd pinot/trino-pinot

docker-compose up -d


# Include Third Eye

  docker run --name thirdeye \
    -p 1426:1426 \
    -p 1427:1427 \
    -d apachepinot/thirdeye:latest ephemeral

docker system prune --all --force --volumes


# Include PGSQL
docker exec -it superset_db bash

pqsl -U superset

CREATE ROLE root SUPERUSER PASSWORD 'root' (Checar comando)

allow privileges in database (checar comando)

CREATE DATABASE kafka_airlines

\c kafka_airlines
CREATE TABLE flights

INSERT INTO flights(id, ori_city,dest_city) VALUES(1,"Rio", "Natal")
INSERT INTO flights(id, ori_city,dest_city) VALUES(2,"Rio", "Natal")
INSERT INTO flights(id, ori_city,dest_city) VALUES(3,"Rio", "Curitiba")

Conect Superset to PGSQL table pela interface UI
Create Queries
Create Chart based on Queries
Create DashBoard based on Charts

# Include KafkaConnector PGSQL

{
  "schema": {
    "type": "struct",
    "fields": [
        { "field": "id", "type": "int", "optional": false },
        { "field": "ori_city", "type": "string", "optional": false },
        { "field": "dest_city", "type": "string", "optional": false }
    ]
  },
  "payload": {
         "id":"1",
         "ori_city":"Rio”,
         "dest_city":"Natal"
  }

  "name": "jdbc-sink-connector",
  "config": {
    "connector.class": "com.ibm.eventstreams.connect.jdbcsink.JDBCSinkConnector",
    "tasks.max": "1",
    "topics": "tidal_data_test",
    "connection.url": "jdbc:postgresql://PGIP:5432/postgres",
    "connection.user": "PGuser",
    "connection.password": "PGpassword",
    "connection.ds.pool.size": 5,
    "insert.mode.databaselevel": true,
    "table.name.format": "tides_table"
  }
}



# Include YugabyteDB / postgresql

docker pull yugabytedb/yugabyte:2.11.2.0-b89

docker run -d --name yugabyte  -p7000:7000 -p9009:9000 -p5433:5433 -p9042:9042 yugabytedb/yugabyte:2.11.2.0-b89 bin/yugabyted start --daemon=false --ui=false

# To persist data mount volume
mkdir ~/yb_data
docker run -d --name yugabyte \
         -p7000:7000 -p9000:9000 -p5433:5433 -p9042:9042 \
         -v ~/yb_data:/home/yugabyte/yb_data \
         yugabytedb/yugabyte:latest bin/yugabyted start \
         --base_dir=/home/yugabyte/yb_data --daemon=false

# SQL SHELL
docker exec -it yugabyte /home/yugabyte/bin/ysqlsh

CREATE DATABASE yb_demo;

\c yb_demo;

\i share/schema.sql
\i share/products.sql
\i share/users.sql
\i share/orders.sql
\i share/reviews.sql

SELECT users.id, users.name, users.email, orders.id, orders.total FROM orders INNER JOIN users ON orders.user_id=users.id LIMIT 10;

docker exec -it yugabyte /home/yugabyte/bin/cqlsh

mkdir -p ~/yb-kafka
git clone https://github.com/yugabyte/yb-kafka-connector.git

mvn clean install -DskipTests





# Stop Flask
Stop the Flask Server with Ctrl-C.

# Stop Kafka
docker-compose down

or Stop the producer and consumer clients with Ctrl-C, if you haven't done so already.
Stop the Kafka broker with Ctrl-C.
Lastly, stop the ZooKeeper server with Ctrl-C.

# Stop all containers docker
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)

# Remove logs
rm -rf /tmp/kafka-logs /tmp/zookeeper





    command: "StartController -zkAddress zookeeper:2181"
    command: "StartBroker -zkAddress zookeeper:2181"
    command: "StartServer -zkAddress zookeeper:2181"
