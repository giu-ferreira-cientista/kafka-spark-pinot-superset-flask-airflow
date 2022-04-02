from pyspark.sql import SparkSession
import pandas as pd
import uuid
import random
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import requests

# Spark session & context
spark = (SparkSession
         .builder
         .master('local')
         .appName('json-ml-predict-consumer')
         # Add kafka package
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1")
         .getOrCreate())
sc = spark.sparkContext

# Create stream dataframe setting kafka server, topic and offset option
df = (spark
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka-server:29092") \
  .option("subscribe", "patient-data") \
  .option("startingOffsets", "earliest") \
  .load())

# read a small batch of data from kafka and display to the console

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
 StructField("timestampstr", TimestampType()),
 StructField("timestamp_epoch", StringType())
 
])

df_json = df.selectExpr('CAST(value AS STRING) as json')

df_json.select(from_json(df_json.json, mySchema).alias('raw_data')) \
  .select('raw_data.nome') \
  .filter("nome is not NULL") \
  .writeStream \
  .trigger(once=True) \
  .format("console") \
  .start() \
  .awaitTermination()

# Test service
import requests
import json

data_jsons = '{"data":"' + 'I love you' + '"}'
print(data_jsons)
result = requests.post('http://127.0.0.1:5000/predict', json=json.loads(data_jsons))
print(json.dumps(result.json()))


def apply_sentiment_analysis(data):
    import requests
    import json
    
    list = [" Loves You", " Hates You"]
    item = random.choice(list)    
    
    data_jsons = '{"data":"' + data + item + '"}'
    
    print(data_jsons)
    
    result = requests.post('http://localhost:5000/predict', json=json.loads(data_jsons))
    return json.dumps(result.json())

vader_udf = udf(lambda data: apply_sentiment_analysis(data), StringType())

schema_output = StructType([StructField('neg', StringType()),\
                            StructField('pos', StringType()),\
                            StructField('neu', StringType()),\
                            StructField('compound', StringType())])


df_json.select(from_json(df_json.json, mySchema).alias('raw_data')) \
  .select('raw_data.nome') \
  .filter("nome is not NULL") \
  . select('nome', \
          from_json(vader_udf('nome'), schema_output).alias('response'))\
  .select('nome', 'response.*') \
  .writeStream \
  .trigger(once=True) \
  .format("console") \
  .start() \
  .awaitTermination()


