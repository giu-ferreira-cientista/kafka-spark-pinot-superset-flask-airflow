# notification_consumer.py
from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
TOPIC_NAME = "NOTIFICATION"
consumer = KafkaConsumer(
    TOPIC_NAME,
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)
def sendNotification(data):
	# process steps
    print(data)

for notification in consumer:
	
	notification_data = notification.value
	
	sendNotification(notification_data)



