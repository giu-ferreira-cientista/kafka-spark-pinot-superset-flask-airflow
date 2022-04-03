from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
TOPIC_NAME = "EMAIL"
KAFKA_SERVER = "kafka-server:29092"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',
    group_id='my-group',
    #enable_auto_commit=False,
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)


def sendEmail(data):
    # process steps
    print(data)
    print("\nE-mail Enviado para o Médico...\n")
    


for email in consumer:
	
	email_data = email.value
	
	sendEmail(email_data)

    
# Parallelism
#with ThreadPoolExecutor(4) as tpool:

#	for email in consumer:

#		email_data = email.value

#		future = tpool.submit(sendEmail, email_data)        

