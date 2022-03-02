#from kafka import KafkaConsumer
#consumer = KafkaConsumer('INFERENCE')
#for msg in consumer:
#    print (msg)


# inference_consumer.py

from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor

TOPIC_NAME = "INFERENCE"

KAFKA_SERVER = "localhost:9092"

NOTIFICATION_TOPIC = "NOTIFICATION"
EMAIL_TOPIC = "EMAIL"

consumer = KafkaConsumer(
    TOPIC_NAME,
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    api_version = (0, 11, 15)
)

def inferenceProcessFunction(data):
    # process steps      
    print(data)
    notification_data = data
    email_data = data
    producer.send(NOTIFICATION_TOPIC, notification_data)
    producer.flush()
    producer.send(EMAIL_TOPIC, email_data)
    producer.flush()



#for msg in consumer:
#    print (msg)

for inf in consumer:    
    inf_data = inf.value        
    inferenceProcessFunction(inf_data)