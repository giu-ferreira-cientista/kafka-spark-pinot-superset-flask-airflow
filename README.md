# Data Pipeline API with Flask, Kafka, Spark, Pinot and Superset 
Repositorio para armazenar os artefatos do projeto de conexao da API em Flask com o Kafka, processamento dos dados via spark e posterior OLAP Realtime with Low Latency com o Pinot e e integração do Dashboard com o Superset para exibição dos gráficos.


# USE DOCKER COMPOSE TO LOAD THE ENVIROMENT - kafka, kafka-ui, jupyter, spark, pinot, superset and airflow


$ chmod +x start.sh


$ ./start.sh





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
- 9000  - Pinot Controller
- 8099  - Pinot Broker
- 8098  - Pinot Server
- 4040  - Spark
- 5000  - Rest API 
- 4000  - Rest API ML


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

# Include Spark Structured Streaming Processing
open 8888 port on your browser

# Shell into spark Container
$ jupyter notebook list

copy and paste token on your browser

# Stop Flask
$ stop the Flask Server with Ctrl-C

# Stop Producers and Consumers
$ stop terminals with Ctrl-C

# Stop all containers docker
$ docker kill $(docker ps -q)
$ docker rm $(docker ps -a -q)
$ docker rmi $(docker images -q)

# Clean and Prune Docler Enviroment
$ docker system prune --all --force --volumes