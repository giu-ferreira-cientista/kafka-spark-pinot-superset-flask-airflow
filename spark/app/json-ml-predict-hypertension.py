from pyspark.sql import SparkSession
import pandas as pd
import uuid
import random
import json
from pyspark.sql.types import *
from pyspark.sql.functions import *
import requests

# Spark session & context
spark = (SparkSession
         .builder
         .master('local')
         .appName('json-ml-predict-hypertension')
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
  .option("group_id", "my-group")   \
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
  .select('raw_data.*') \
  .filter("nome is not NULL") \
  .writeStream \
  .trigger(once=True) \
  .format("console") \
  .start() 
  #.awaitTermination()

# Test service
#data_jsons = '{"data":"' + 'I love you' + '"}'
#print(data_jsons)
#result = requests.post('http://127.0.0.1:5000/predict', json=json.loads(data_jsons))
#print(json.dumps(result.json()))


def predict_hypertension(patient):
    
    patient_dict = {}
    patient_dict['id'] = patient[0]
    patient_dict['nome'] = patient[1]
    patient_dict['idade'] = patient[2]
    patient_dict['sexo'] = patient[3]
    patient_dict['peso'] = patient[4]
    patient_dict['altura'] = patient[5]
    patient_dict['bpm'] = patient[6]
    patient_dict['pressao'] = patient[7]
    patient_dict['respiracao'] = patient[8]
    patient_dict['temperatura'] = patient[9]
    patient_dict['glicemia'] = patient[10]
    patient_dict['saturacao_oxigenio'] = patient[11]
    patient_dict['estado_atividade'] = patient[12]
    patient_dict['dia_de_semana'] = patient[13]
    patient_dict['periodo_do_dia'] = patient[14]
    patient_dict['semana_do_mes'] = patient[15]
    patient_dict['estacao_do_ano'] = patient[16]
    patient_dict['passos'] = patient[17]
    patient_dict['calorias'] = patient[18]
    patient_dict['distancia'] = patient[19]
    patient_dict['tempo'] = patient[20]
    patient_dict['total_sleep_last_24'] = patient[21]
    patient_dict['deep_sleep_last_24'] = patient[22]
    patient_dict['light_sleep_last_24'] = patient[23]
    patient_dict['awake_last_24'] = patient[24]
    patient_dict['fumante'] = patient[25]
    patient_dict['genetica'] = patient[26]
    patient_dict['gestante'] = patient[27]
    patient_dict['frutas'] = patient[28]
    patient_dict['vegetais'] = patient[29]
    patient_dict['alcool'] = patient[30]
    patient_dict['doenca_coracao'] = patient[31]
    patient_dict['avc'] = patient[32]
    patient_dict['colesterol_alto'] = patient[33]
    patient_dict['exercicio'] = patient[34]
    patient_dict['timestampstr'] = patient[35]
    patient_dict['timestamp_epoch'] = patient[36]

    data_jsons = json.dumps(patient_dict)

    print()
    print(data_jsons)
    print()

    result = requests.post('http://localhost:5000/predict-hypertension', json=data_jsons)
        
    result_json = json.dumps(result.json().replace("[","").replace("]",""))

    result_json = result_json.replace('\\', '')[1:-1]
    
    print()
    print(result_json)
    print()
    
    return result_json

vader_udf = udf(lambda patient: predict_hypertension(patient), StringType())

schema_output = StructType([StructField('label', IntegerType()),\
                            StructField('score', DoubleType())])

df_json.select(from_json(df_json.json, mySchema).alias('raw_data')) \
  .select('raw_data.*') \
  .filter("nome is not NULL") \
  .select('nome', \
          from_json(vader_udf(array('*')), schema_output).alias('response'))\
  .select('nome', 'response.*') \
  .writeStream \
  .trigger(once=True) \
  .format("console") \
  .start() \
  .awaitTermination()


df_json.select(from_json(df_json.json, mySchema).alias('raw_data')) \
  .select('raw_data.*') \
  .filter("nome is not NULL") \
  .select('nome', \
          from_json(vader_udf(array('*')), schema_output).alias('response'))\
  .select('nome', 'response.*') \
  .select(
      expr("CAST(nome AS STRING)").alias("key"),
      expr("'{\"label\":' || CAST(label AS STRING) || ',' || '\"score\":' || CAST(score AS STRING) || '}'").alias("value")            
   ) \
  .writeStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka-server:29092") \
  .option("checkpointLocation", "/home/jovyan/work/json/predict_hypertension") \
  .option("topic", "predict-hypertension-data")        \
  .start()  \
  .awaitTermination()

