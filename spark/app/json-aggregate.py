from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DoubleType, TimestampType 	



# Spark session & context
spark = (SparkSession
         .builder
         .master('local')
         .appName('json-aggregator')
         # Add kafka package
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1")
         .getOrCreate())
sc = spark.sparkContext




df = (spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "kafka-server:29092") # kafka server
  .option("subscribe", "patient-data") # topic
  .option("startingOffsets", "earliest") # start from beginning
  .option("failOnDataLoss", False)
  .load())



# create schema for patient
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

# extract data and ensure `eventTime` is timestamp
df = (
    df.selectExpr("CAST(value as string)")
      .select(F.from_json(F.col("value"),mySchema).alias("json_value"))
      .selectExpr("json_value.*") # gives us a dataframe with columns (eventTime,temperatura, etc...)
      .select(
          F.expr("CAST(timestampstr as timestamp)").alias("eventTime"),
          F.col("nome"),
          F.col("temperatura"),
          F.col("bpm"),
          F.col("pressao"),
          F.col("respiracao"),
          F.col("glicemia"),
          F.col("saturacao_oxigenio")
      )
      
)


# when using window you will get a range or value resembling [start,end]. 
# I have chosen the `start` for this example
from pyspark.sql.functions import col, window

windowedAvg = ( 
    df.withWatermark("eventTime", "5 minutes") 
      .groupBy(window(F.col("eventTime"), "5 minutes").alias('eventTimeWindow'), F.col("nome"))
      .agg(F.avg("temperatura").alias("avgtemperature"),F.avg("bpm").alias("avgbpm"),F.avg("pressao").alias("avgpressao"),F.avg("respiracao").alias("avgrespiracao"),F.avg("glicemia").alias("avgglicemia"),F.avg("saturacao_oxigenio").alias("avgsaturacao_oxigenio") )       
      .orderBy(F.col("eventTimeWindow"))
      .select(
          F.col("eventTimeWindow.start").alias("eventTime"),
          F.col("nome"),
          F.col("avgtemperature"),
          F.col("avgbpm"),
          F.col("avgpressao"),
          F.col("avgrespiracao"),
          F.col("avgglicemia"),
          F.col("avgsaturacao_oxigenio")
          
      )
)


# continue with your code to write to your various streams
query = windowedAvg\
        .select(
            F.expr("CAST(eventTime AS STRING)").alias("key"),
            F.expr("'{\"eventTime\":\"' || CAST(eventTime AS STRING) || '\",' || '\"nome\":\"' || CAST(nome AS STRING) || '\",' || '\"avgbpm\":' || CAST(avgbpm AS STRING) || ',' || '\"avgtemp\":' || CAST(avgtemperature AS STRING) || ',' || '\"avgrespiracao\":' || CAST(avgrespiracao AS STRING) || ',' || '\"avgglicemia\":' || CAST(avgglicemia AS STRING) || ',' || '\"avgpressao\":' || CAST(avgpressao AS STRING) || ',' || '\"avgsaturacao_oxigenio\":' || CAST(avgsaturacao_oxigenio AS STRING) || '}'").alias("value")            
        ) \
        .writeStream\
        .outputMode('complete')\
        .format('console')\
        .option('truncate', 'true')\
        .start()



# write on kafka topic avgtemperature
# here i've chosen as an example to use the eventTime as the key and the value to be the avgtemperature
qk = (windowedAvg 
        .select(
            F.expr("CAST(eventTime AS STRING)").alias("key"),
            F.expr("'{\"eventTime\":\"' || CAST(eventTime AS STRING) || '\",' || '\"nome\":\"' || CAST(nome AS STRING) || '\",' || '\"avgbpm\":' || CAST(avgbpm AS STRING) || ',' || '\"avgtemp\":' || CAST(avgtemperature AS STRING) || ',' || '\"avgrespiracao\":' || CAST(avgrespiracao AS STRING) || ',' || '\"avgglicemia\":' || CAST(avgglicemia AS STRING) || ',' || '\"avgpressao\":' || CAST(avgpressao AS STRING) || ',' || '\"avgsaturacao_oxigenio\":' || CAST(avgsaturacao_oxigenio AS STRING) || '}'").alias("value")            
        ) 
        .writeStream 
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka-server:29092") 
        .option("checkpointLocation", "/home/jovyan/work/json/aggregate") 
        .option("topic", "avg-data")        
        .outputMode("complete") 
        .start())

qk.awaitTermination()        
#query.awaitTermination()


