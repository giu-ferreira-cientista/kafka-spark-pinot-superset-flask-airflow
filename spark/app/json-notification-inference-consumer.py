# csv_inference_consumer.py

from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor



TOPIC_NAME = "avg-data"

KAFKA_SERVER = "kafka-server:29092"

NOTIFICATION_TOPIC = "NOTIFICATION"



consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)


producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    api_version = (0, 11, 15)
)

def inferenceProcessFunction(data):
    # process steps with data in json format      
    
    json_data = json.loads(data)
    
    print("eventTime:" + str(json_data['eventTime']) + ' / ' + "nome:" + str(json_data['nome']) + ' / ' + "bpm:" + str(json_data['avgbpm']) + ' / ' + "temp:" + str(json_data['avgtemp']))
    
    if(json_data['avgbpm'] >= 120 or json_data['avgtemp'] >= 38):
        notification_data = data        
        producer.send(NOTIFICATION_TOPIC, notification_data)
        producer.flush()
        print('\nNotification Topic Sent!\n')
    

for inf in consumer:
    print('processing line...')
    inf_data = inf.value        
    inferenceProcessFunction(inf_data)



