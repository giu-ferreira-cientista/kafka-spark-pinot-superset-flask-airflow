# Event producer

import json
from sseclient import SSEClient as EventSource
from kafka import KafkaProducer

# Create producer
producer = KafkaProducer(
    bootstrap_servers='kafka-server:29092', # kafka server ip address inspect - something like 172.23.0.5
    value_serializer=lambda v: json.dumps(v).encode('utf-8') #json serializer
    )

# Read streaming event
url = 'https://api.mockaroo.com/api/e172bfb0?count=1000&key=42e8f800'
try:
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                #Send msg to topic wiki-changes
                producer.send('patient-data', change)

except KeyboardInterrupt:
    print("process interrupted")
