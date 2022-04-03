# import libraries
#import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DoubleType
import time
import os

# Spark session & context
spark = (SparkSession
         .builder
         .master('local')
         .appName('json-producer')
         # Add kafka package
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1")
         .getOrCreate())
sc = spark.sparkContext

mySchema = StructType([
 StructField("id", IntegerType()),
 StructField("nome", StringType()),
 StructField("idade", IntegerType()),
 StructField("sexo", IntegerType()),
 StructField("peso", DoubleType()),
 StructField("altura", IntegerType()),
 StructField("bpm", DoubleType()),
 StructField("pressao", DoubleType()),
 StructField("respiracao", DoubleType()),
 StructField("temperatura", DoubleType()),
 StructField("glicemia", DoubleType()),
 StructField("saturacao_oxigenio", DoubleType()),
 StructField("estado_atividade", IntegerType()),
 StructField("dia_de_semana", IntegerType()),
 StructField("periodo_do_dia", IntegerType()),
 StructField("semana_do_mes", IntegerType()),
 StructField("estacao_do_ano", IntegerType()),
 StructField("passos", IntegerType()),
 StructField("calorias", DoubleType()),
 StructField("distancia", DoubleType()),
 StructField("tempo", DoubleType()),
 StructField("total_sleep_last_24", DoubleType()),
 StructField("deep_sleep_last_24", DoubleType()),
 StructField("light_sleep_last_24", DoubleType()),
 StructField("awake_last_24", DoubleType()), 
 StructField("fumante", IntegerType()),
 StructField("genetica", IntegerType()),
 StructField("gestante", IntegerType()),
 StructField("frutas", IntegerType()),
 StructField("vegetais", IntegerType()),
 StructField("alcool", IntegerType()),
 StructField("doenca_coracao", IntegerType()),     
 StructField("avc", IntegerType()),
 StructField("colesterol_alto", IntegerType()),  
 StructField("exercicio", IntegerType()),  
 StructField("timestampstr", StringType()),
 StructField("timestamp_epoch", StringType())    
])


while True:
    print("loop")
    timestr = time.strftime("%Y%m%d-%H%M%S")

    json_name = "patient-data-" + timestr + '.json' 

    os.system('curl "https://api.mockaroo.com/api/e172bfb0?count=5&key=42e8f800" > ' + json_name)

    os.system('mv ' + json_name + ' /home/jovyan/work/json')



    json_path = "/home/jovyan/work/json"
    json_topic = "patient-data"
    kafka_server = "kafka-server:29092"

    streamingDataFrame = spark.readStream.schema(mySchema).json(json_path)

    streamingDataFrame.selectExpr("CAST(id AS STRING) AS key", "to_json(struct(*)) AS value") \
      .writeStream \
      .format("kafka") \
      .option("topic", json_topic) \
      .option("kafka.bootstrap.servers", kafka_server) \
      .option("checkpointLocation", json_path) \
      .start()

    time.sleep(10)


