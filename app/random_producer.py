import json 
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer()

num_records = 500

for count in range(num_records):
    print(time.ctime())
    # Prints the current time with a one second difference
    time.sleep(1)    
    nome = 'Joe'
    bpm = random.randint(60, 170)
    
    # Data to be written 
    dictionary ={ 
    "id": count, 
    "name": nome, 
    "bpm": bpm
    } 

    # Serializing json  
    json_object = json.dumps(dictionary).encode('utf-8')
    print(json_object)
    
    #my_str = 'alemao'
    
    #message_bytes = str.encode(my_str)

    producer.send('INFERENCE', json_object)
    producer.flush()
