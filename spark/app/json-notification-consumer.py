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
    group_id='my-group',
    auto_offset_reset='earliest',
    #enable_auto_commit=False,
    # to deserialize kafka.producer.object into dict
    #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

def sendNotification(data):
	# process steps
    print(data)
    json_data = json.loads(data)

    if(json_data['avgbpm'] >= 130):
        print("\nALERTA RECEBIDO! Cheque seus batimentos cardiacos! (avgbpm >= 130)\n")

    if(json_data['avgtemp'] >= 39):
        print("\nALERTA RECEBIDO! Cheque sua temperatura! (avgtemp >= 39)\n")

    if(json_data['avgpressao'] >= 14):
        print("\nALERTA RECEBIDO! Cheque sua pressao! (avgpressao >= 14)\n")

    if(json_data['avgrespiracao'] >= 20):
        print("\nALERTA RECEBIDO! Cheque sua frequencia respiratoria! (avgrespiracao >= 20)\n")

    if(json_data['avgglicemia'] >= 160):
        print("\nALERTA RECEBIDO! Cheque sua glicemia! (avgglicemia >= 160)\n")

    if(json_data['avgsaturacao_oxigenio'] <= 93):
        print("\nALERTA RECEBIDO! Cheque sua saturação do oxigenio! (avgsaturacao_oxigenio <= 93)\n")
   

for notification in consumer:
	
	notification_data = notification.value
	
	sendNotification(notification_data)


