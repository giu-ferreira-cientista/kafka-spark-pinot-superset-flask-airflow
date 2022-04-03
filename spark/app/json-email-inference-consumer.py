# csv_inference_consumer.py

from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor


TOPIC_NAME = "avg-data"

KAFKA_SERVER = "kafka-server:29092"

EMAIL_TOPIC = "EMAIL"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='my-group',
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)


producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    api_version = (0, 11, 15)
)

def inferenceProcessFunction(data):
    # process steps with data in json format      
    
    #df = pd.DataFrame.from_dict(data)
    #hourly_avg = df.groupby(df['timestampstr'].dt.hour)['pressure'].mean()
    #print(hourly_avg)
    
    json_data = json.loads(data)
    
    print("eventTime:" + str(json_data['eventTime']) + ' / ' + "nome:" + str(json_data['nome']) + ' / ' + "bpm:" + str(json_data['avgbpm']) + ' / ' + "temp:" + str(json_data['avgtemp']))
        
    email_data = data
    producer.send(EMAIL_TOPIC, email_data)
    producer.flush()
    print('\nEmail topic Sent!\n')



for inf in consumer:
    print('processing line...')
    inferenceProcessFunction(inf.value)

