# app.py

from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from subprocess import Popen
from kafka import KafkaConsumer, KafkaProducer
import urllib.parse
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


app = Flask(__name__)
sid = SentimentIntensityAnalyzer()


@app.route('/', methods=['GET'])
def root():

    print("Executing Root...")
        
    return jsonify({
        "message": "Api Execcuting OK", 
        "status": "Pass"})


@app.route('/execute-api', methods=['GET'])
def execute_api():

    print("Executing Command...")
    
    cmd = 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5,io.delta:delta-core_2.12:0.7.0 --master local[*] --driver-memory 12g --executor-memory 12g /home/jovyan/work/app/event-producer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command API Executed OK", 
        "status": "Pass"})


@app.route('/execute-csv', methods=['GET'])
def execute_csv():

    print("Executing Command...")
    
    cmd = 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5,io.delta:delta-core_2.12:0.7.0 --master local[*] --driver-memory 12g --executor-memory 12g /home/jovyan/work/app/csv-producer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command CSV Executed OK", 
        "status": "Pass"})

@app.route('/execute-json-producer', methods=['GET'])
def execute_json_producer():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/json-producer-loop.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command JSON Producer Executed OK", 
        "status": "Pass"})

@app.route('/execute-json-aggregate', methods=['GET'])
def execute_json_aggregate():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/json-aggregate.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command JSON Aggregate Executed OK", 
        "status": "Pass"})


@app.route('/execute-json-notification-inference', methods=['GET'])
def execute_json_notification_inference():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/json-notification-inference-consumer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command JSON Notification Inference Executed OK", 
        "status": "Pass"})


@app.route('/execute-json-email-inference', methods=['GET'])
def execute_json_email_inference():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/json-email-inference-consumer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command JSON Email Inference Executed OK", 
        "status": "Pass"})

@app.route('/execute-json-notification-consumer', methods=['GET'])
def execute_json_notification_consumer():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/json-notification-consumer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command JSON Notification Consumer Executed OK", 
        "status": "Pass"})



@app.route('/execute-json-email-consumer', methods=['GET'])
def execute_json_email_consumer():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/json-email-consumer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command JSON Email Consumer Executed OK", 
        "status": "Pass"})



@app.route('/execute-csv-inference', methods=['GET'])
def execute_csv_inference():

    print("Executing Command...")
    
    cmd = 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5,io.delta:delta-core_2.12:0.7.0 --master local[*] --driver-memory 12g --executor-memory 12g /home/jovyan/work/app/csv-inference-consumer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command CSV Inference Executed OK", 
        "status": "Pass"})


@app.route('/getData', methods=['GET'])
def kafkaConsumer():

    KAFKA_SERVER = "kafka-server:29092"
    CONSUMER_TOPIC_NAME = "NOTIFICATION"
    consumer = KafkaConsumer(
        CONSUMER_TOPIC_NAME,
        bootstrap_servers=[KAFKA_SERVER],
        # to deserialize kafka.producer.object into dict
        #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

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



@app.route('/predict', methods=['POST'])
def predict():
    result = sid.polarity_scores(request.get_json()['data'])
    return jsonify(result)





if __name__ == "__main__":
    app.run(debug=True, port = 5000, host='0.0.0.0')