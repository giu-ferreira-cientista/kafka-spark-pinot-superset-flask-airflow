from pyspark.sql import SparkSession

# Spark session & context
spark = (SparkSession
         .builder
         .master('local')
         .appName('json-changes-dataviz')
         .config("spark.sql.streaming.schemaInference", True) #Stream dataframe infers schema
         .getOrCreate())
sc = spark.sparkContext

# Read parquet stream
df_stream = (
    spark
    .readStream
    .format("parquet")
    .load("/home/jovyan/work/data-lake/json-changes")
)

# Create dataframe grouping by window 
from pyspark.sql.functions import window, col, current_timestamp

df_count = (
    df_stream
    .withWatermark("change_timestamp", "10 minutes") # Don't aggregate events arriving more than 10 minutes late
    .groupBy(
        window(col("change_timestamp"), "10 minutes", "10 minutes"), # 10 minute window, updating every 10 minutes
        col("nome"))
    .count()
)

# Create query stream with memory sink
queryStream = (df_count
 .writeStream
 .format("memory")
 .queryName("json_changes_ingestion")
 .outputMode("update")
 .start())

from time import sleep
from IPython.display import clear_output
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rc('font', family='DejaVu Sans')
sns.set(style="whitegrid")


try:
    i=1
    while True:
        # Clear output
        clear_output(wait=True)
        print("**********************")
        print("General Info")
        print("**********************")
        print("Run:{}".format(i))
        if (len(queryStream.recentProgress) > 0):
            print("Stream timestamp:{}".format(queryStream.lastProgress["timestamp"]))
            print("Watermark:{}".format(queryStream.lastProgress["eventTime"]["watermark"]))
            print("Total Rows:{}".format(queryStream.lastProgress["stateOperators"][0]["numRowsTotal"]))
            print("Updated Rows:{}".format(queryStream.lastProgress["stateOperators"][0]["numRowsUpdated"]))
            print("Memory used MB:{}".format((queryStream.lastProgress["stateOperators"][0]["memoryUsedBytes"]) * 0.000001))
            
        df = spark.sql(
                """
                    select
                        window.start
                        ,window.end
                        ,nome                        
                    from
                        json_changes
                    where
                        window.start = (select max(window.start) from json_changes)
                    group by
                        window.start
                        ,window.end
                        ,nome
                    order by
                        3 desc
                    limit 10
                """
        ).toPandas()

        # Plot the total crashes
        sns.set_color_codes("muted")

        # Initialize the matplotlib figure
        plt.figure(figsize=(8,6))

        print("**********************")
        print("Graph - Top 10 users")
        print("**********************")
        try:
            # Barplot
            sns.barplot(x="count", y="nome", data=df)

            # Show barplot
            plt.show()
        except ValueError:
            # If Dataframe is empty, pass
            pass

        print("**********************")
        print("Table - Top 10 users")
        print("**********************")
        display(df)
        
        print("**********************")
        print("Table - Count by aggregation window")
        print("**********************")
        df1 = spark.sql(
                """
                    select
                        window.start
                        ,window.end                        
                        ,count(distinct nome) qty_users
                    from
                        json_changes
                    group by
                        window.start
                        ,window.end
                    order by
                        window.start desc
                """
        ).toPandas()
        
        display(df1)
        
        sleep(10)
        i=i+1
except KeyboardInterrupt:
    print("process interrupted.")

# Check active streams
for s in spark.streams.active:
    print("ID:{} | NAME:{}".format(s.id, s.name))

# Stop stream
queryStream.stop()


