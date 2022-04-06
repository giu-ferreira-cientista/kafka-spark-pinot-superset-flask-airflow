# Data Pipeline API with Flask, Kafka, Spark, Pinot and Superset 
Repositorio para armazenar os artefatos do projeto de conexao da API em Flask com o Kafka, processamento dos dados via spark e posterior OLAP Realtime with Low Latency com o Pinot e e integração do Dashboard com o Superset para exibição dos gráficos.


# HOW TO LOAD ALL THE ENVIROMENT - kafka, kafka-ui, jupyter, spark, pinot, superset and airflow

# Make scripts executable
$ chmod +x _up.sh _down.sh _start.sh _stop.sh 

# Build all and Compose up
$ ./_up.sh

# Start an existing compose
$ ./_start.sh

# Stop an existing compose
$ ./_stop.sh

# Compose down and remove all containers
$ ./_down.sh


Start airflow at port 8080 and run dags tagged with 'pipeline'

Main Published Ports:
- 8081 - Kafka-Ui
- 9000 - Pinot
- 8888 - Jupyter / Pyspark Notebook
- 8088 - Superset

Main Services Ports:
- 9092  - Kafka
- 29092 - Kafka Broker
- 2181  - Zookeeper
- 9000  - Pinot Controller
- 8099  - Pinot Broker
- 8098  - Pinot Server
- 4040  - Spark
- 5000  - Rest API 

# Open Jupyter with Spark Structured Streaming Processing
open 8888 port on your browser

# Shell into Spark Container
$ jupyter notebook list

copy and paste token on your browser

# How to Stop Services
# Stop Flask API in Saprk container
stop the Flask Server with Ctrl-C

# Stop possible running Producers and Consumers
stop terminals with Ctrl-C

# Stop all containers docker
$ docker kill $(docker ps -q)
$ docker rm $(docker ps -a -q)
$ docker rmi $(docker images -q)

# Clean and Prune Docker Enviroment
$ docker system prune --all --force --volumes

