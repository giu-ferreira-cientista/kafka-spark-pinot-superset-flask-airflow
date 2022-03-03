# Data Pipeline API with Flask, Kafka, Spark, Pinot and Superset 
Repositorio para armazenar os artefatos do projeto de conexao da API em Flask com o Kafka, processamento dos dados via spark e posterior OLAP Realtime with Low Latency com o Pinot e criação do Dashboard com o Superset para exibição de gráficos

# USE DOCKER COMPOSE TO LOAD THE ENVIROMENT - kafka, kafka-ui, jupyter, spark, pinot and superset 
$ docker-compose docker-compose_kafka_spark_pinot_superset.yaml up -d

Main Published Ports:
- 8081 - Kafka-Ui
- 9000 - Pinot
- 8888 - Jupyter / Pyspark Notebook
- 8088 - Superset

# Create Pinot Table Schema
$ docker cp pinot/examples/airlineStats_realtime_table_config.json manual-pinot-controller:/opt/pinot/examples/airlineStats_realtime_table_config.json

# Inspect into manual-pinot-controller and Add Table
$ bin/pinot-admin.sh AddTable \
    -schemaFile examples/stream/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/airlineStats_realtime_table_config.json \
    -exec    

# Configure Superset Enviroment
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

# Add Pinot Superset Database through the Superset UI (Replace the ip with your pinot broker and controller)
pinot+http://172.29.0.12:8099/query?server=http://172.29.0.8:9000/

# Load Sample Data into Kafka Topic and Query Pinot and Superset Again!
{"Quarter":1,"FlightNum":1,"Origin":"JFK","LateAircraftDelay":null,"DivActualElapsedTime":null,"DivWheelsOns":null,"DivWheelsOffs":null,"ArrDel15":0,"AirTime":359,"DivTotalGTimes":null,"DepTimeBlk":"0900-0959","DestCityMarketID":32575,"DaysSinceEpoch":16071,"DivAirportSeqIDs":null,"DepTime":914,"Month":1,"DestStateName":"California","CRSElapsedTime":385,"Carrier":"AA","DestAirportID":12892,"Distance":2475,"ArrTimeBlk":"1200-1259","SecurityDelay":null,"DivArrDelay":null,"LongestAddGTime":null,"OriginWac":22,"WheelsOff":934,"UniqueCarrier":"AA","DestAirportSeqID":1289203,"DivReachedDest":null,"Diverted":0,"ActualElapsedTime":384,"AirlineID":19805,"OriginStateName":"New York","FlightDate":"2014-01-01","DepartureDelayGroups":0,"DivAirportLandings":0,"OriginCityName":"New York, NY","OriginStateFips":36,"OriginState":"NY","DistanceGroup":10,"WeatherDelay":null,"DestWac":91,"WheelsOn":1233,"OriginAirportID":12478,"OriginCityMarketID":31703,"NASDelay":null,"DestState":"CA","ArrTime":1238,"ArrivalDelayGroups":0,"Flights":1,"DayofMonth":1,"RandomAirports":["SEA","PSC","PHX","MSY","ATL","TYS","DEN","CHS","PDX","LAX","EWR","SFO","PIT","RDU","RAP","LSE","SAN","SBN","IAH","OAK","BRO","JFK","SAT","ORD","ACY","DFW","BWI","TPA","BFL","BOS","SNA","ISN"],"TotalAddGTime":null,"CRSDepTime":900,"DayOfWeek":3,"Dest":"LAX","CancellationCode":null,"FirstDepTime":null,"DivTailNums":null,"DepDelayMinutes":14,"DepDelay":14,"TaxiIn":5,"OriginAirportSeqID":1247802,"DestStateFips":6,"ArrDelay":13,"Cancelled":0,"DivAirportIDs":null,"TaxiOut":20,"DepDel15":0,"CarrierDelay":null,"DivLongestGTimes":null,"DivAirports":null,"DivDistance":null,"Year":2014,"CRSArrTime":1225,"ArrDelayMinutes":13,"TailNum":"N338AA","DestCityName":"Los Angeles, CA"}


# Running the Flask API Producers and Consumers

# Create Kafka Topics

$ bin/kafka-topics.sh --create --topic INFERENCE --bootstrap-server localhost:9092
or
$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic INFERENCE

$ bin/kafka-topics.sh --create --topic EMAIL --bootstrap-server localhost:9092

$ bin/kafka-topics.sh --create --topic NOTIFICATION --bootstrap-server localhost:9092

# Console - Produce some events
$ bin/kafka-console-producer.sh --topic INFERENCE --bootstrap-server localhost:9092

# Console - Open Consumer
$ bin/kafka-console-consumer.sh --topic INFERENCE --from-beginning --bootstrap-server localhost:9092

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

# Stop Flask
$ stop the Flask Server with Ctrl-C.

# Stop Producers and Consumers
$ stop terminals with Ctrl-C.

# Stop Kafka
$ docker-compose docker-compose_kafka_spark_pinot_superset.yaml down

# Stop all containers docker
$ docker kill $(docker ps -q)
$ docker rm $(docker ps -a -q)
$ docker rmi $(docker images -q)

# Clean and Prune Docler Enviroment
$ docker system prune --all --force --volumes