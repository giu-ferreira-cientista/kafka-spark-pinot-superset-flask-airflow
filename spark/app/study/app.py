# app.py

from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from kafka import KafkaConsumer, KafkaProducer
import urllib.parse

app = Flask(__name__)
PRODUCER_TOPIC_NAME = "INFERENCE"
KAFKA_SERVER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    api_version = (0, 11, 15)    
)

CONSUMER_TOPIC_NAME = "NOTIFICATION"
consumer = KafkaConsumer(
CONSUMER_TOPIC_NAME,
auto_offset_reset='earliest', 
enable_auto_commit=True,
auto_commit_interval_ms=1000, group_id='my-group'
# to deserialize kafka.producer.object into dict
#value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)


@app.route('/kafka/pushToConsumers', methods=['POST'])
def kafkaProducer():

    req = request.get_data()
    # gets the Dictionary and value list
    res = urllib.parse.parse_qs(req.decode('utf8'))
    
    # Data to be written 
    dictionary ={ 
    "id": res['id'], 
    "name": res['name'], 
    "bpm": res['bpm']
    } 

    # Serializing json  
    json_object = json.dumps(dictionary).encode('utf-8')
    print(json_object)
    
	#push data into INFERENCE TOPIC    
    producer.send(PRODUCER_TOPIC_NAME, json_object)
    producer.flush()
    print("Sent to consumer")
    return jsonify({
        "message": "You will receive an email in a short while with the plot", 
        "status": "Pass"})

@app.route('/kafka/getData', methods=['GET'])
def kafkaConsumer():

    data_response = []

    def sendNotification(data):
        # process steps
        data_response.append(data.decode('utf-8'))

    retries = 1
    while retries <= 1:        
        msg_pack = consumer.poll(timeout_ms=500)

        for tp, messages in msg_pack.items():
            for message in messages:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                    message.offset, message.key,
                                                    message.value))
                sendNotification(message.value)
        retries += 1
        
    
    print("Sent to consumer")
    
    return jsonify({
        "message": data_response, 
        "status": "Pass"})
    

if __name__ == "__main__":
    app.run(debug=True, port = 5000)