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
    group_id='my-group',
    #enable_auto_commit=False,
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
    
    print("eventTime:" + str(json_data['eventTime']) + ' / ' + "nome:" + str(json_data['nome']) + ' / ' + "bpm:" + str(json_data['avgbpm']) + ' / ' + "temp:" + str(json_data['avgtemp']) + ' / ' + "pressao:" + str(json_data['avgpressao']) + ' / ' + "respiracao:" + str(json_data['avgrespiracao']) + ' / ' + "glicemia:" + str(json_data['avgglicemia']) + ' / ' + "saturacao_oxigenio:" + str(json_data['avgsaturacao_oxigenio']))
    
    if(json_data['avgbpm'] >= 130 or json_data['avgtemp'] >= 39 or json_data['avgpressao'] >= 14 or json_data['avgrespiracao'] >= 20 or json_data['avgglicemia'] >= 160 or json_data['avgsaturacao_oxigenio'] <= 93 ):
        notification_data = data        
        producer.send(NOTIFICATION_TOPIC, notification_data)
        producer.flush()
        print('\nNotification Topic Sent!\n')
    

for inf in consumer:
    print('processing line...')
    inf_data = inf.value        
    inferenceProcessFunction(inf_data)



