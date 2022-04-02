# notification_consumer.py
from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
TOPIC_NAME = "NOTIFICATION"
KAFKA_SERVER = "kafka-server:29092"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    enable_auto_commit=False,
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

def sendNotification(data):
	# process steps
    print(data)
    json_data = json.loads(data)

    if(json_data['avgbpm'] >= 120):
        print("\nALERTA RECEBIDO! Cheque seus batimentos cardiacos! (BPM >= 120)\n")

    if(json_data['avgtemp'] >= 38):
        print("\nALERTA RECEBIDO! Cheque sua temperatura! (T >= 38)\n")

    if(json_data['avgpressao'] >= 13):
        print("\nALERTA RECEBIDO! Cheque sua pressao! (P >= 13)\n")

    if(json_data['avgrespiracao'] >= 20):
        print("\nALERTA RECEBIDO! Cheque sua frequencia respiratoria! (F >= 20)\n")

    if(json_data['avgglicemia'] >= 100):
        print("\nALERTA RECEBIDO! Cheque sua glicemia! (G >= 100)\n")

    if(json_data['avgsaturacao_oxigenio'] <= 94):
        print("\nALERTA RECEBIDO! Cheque sua saturação do oxigenio! (S <= 94)\n")
   

for notification in consumer:
	
	notification_data = notification.value
	
	sendNotification(notification_data)


