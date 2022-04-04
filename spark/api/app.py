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
from pycaret.classification import *
import pandas as pd
import pickle

app = Flask(__name__)
sid = SentimentIntensityAnalyzer()

DB_model = load_model('/home/jovyan/work/api/DB_model')

HT_model = load_model('/home/jovyan/work/api/HT_model')

df_total = pd.read_csv("/home/jovyan/work/api/populacao.csv")

df_total['Diabetes_012'] = ""

exp_clf101 = setup(data = df_total, target = 'Diabetes_012', use_gpu=False, silent=True)

@app.route('/', methods=['GET'])
def root():

    print("Executing Root...")
        
    return jsonify({
        "message": "Api Executing OK", 
        "status": "Pass"})


@app.route('/execute-api', methods=['GET'])
def execute_api():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/event-producer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command API Executed OK", 
        "status": "Pass"})


@app.route('/execute-csv-producer', methods=['GET'])
def execute_csv():

    print("Executing Command...")
    
    cmd = 'python /home/jovyan/work/app/csv-producer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command CSV Producer Executed OK", 
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
    
    print()
    print(result)
    print()

    return jsonify(result)

@app.route('/predict-diabetes', methods=['POST'])
def predict_diabetes():

    paciente = request.get_json()
    
    print(paciente)

    #paciente = json.loads(paciente)
    # {"id": 1,  "nome": "joao",  "idade": 34,  "sexo": 0,  "peso": 84,  "altura": 170,  "bpm": 92,  "pressao": 146,  "respiracao": 11,  "temperatura": 37,  "glicemia": 128,  "saturacao_oxigenio": 98,  "estado_atividade": 2,  "dia_de_semana": 1,  "periodo_do_dia": 1,  "semana_do_mes": 2,  "estacao_do_ano": 3,  "passos": 303,  "calorias": 24.24,  "distancia": 378.75,  "tempo": 4.848,  "total_sleep_last_24": 6,  "deep_sleep_last_24": 5,  "light_sleep_last_24": 3,  "awake_last_24": 15,  "fumante": 1,  "genetica": 1,  "gestante": 0,  "frutas": 0,  "vegetais": 0,  "alcool": 1,  "doenca_coracao": 1,  "avc": 1,  "colesterol_alto": 1,  "exercicio": 0,  "timestampstr": "2022-03-20 11:19:28",  "timestamp_epoch": "1647775168"}

    data_teste = pd.DataFrame()
    if(float(paciente["pressao"]) > 12):
        high_bp = 0
    else:
        high_bp = 1
    data_teste['HighBP'] = [float(high_bp)]  
    data_teste['HighChol'] = [float(paciente["colesterol_alto"])]
    data_teste['BMI'] = [float(float(paciente["peso"]) / (float(paciente["altura"]) / 100) ** 2)]
    data_teste['Smoker'] = [float(paciente["fumante"])] 
    data_teste['Stroke'] = [float(paciente["avc"])]
    data_teste['HeartDiseaseorAttack'] = [float(paciente["doenca_coracao"])] 
    data_teste['Fruits'] = [float(paciente["frutas"])] 
    data_teste['Veggies'] = [float(paciente["vegetais"])]
    data_teste['HvyAlcoholConsump'] = [float(paciente["alcool"])]
    data_teste['Sex'] = [float(paciente["sexo"])]
    data_teste['PhysActivity'] = [float(paciente["exercicio"])]
    data_teste['Age'] = [float(paciente["idade"])]
    data_teste['Diabetes_012'] = [""]

    
    print(data_teste['HighBP'])
    print(data_teste['HighChol'])
    print(data_teste['BMI'])
    print(data_teste['Smoker'])
    print(data_teste['Stroke'])
    print(data_teste['HeartDiseaseorAttack'])
    print(data_teste['Fruits'])
    print(data_teste['Veggies'])
    print(data_teste['HvyAlcoholConsump'])
    print(data_teste['Sex'])
    print(data_teste['PhysActivity'])
    print(data_teste['Age'])

    #realiza a predição.
    result = predict_model(DB_model, data=data_teste)

    #recupera os resultados.
    label = result["Label"][0]
    score = result["Score"][0]*100

    print(label)
    print(score)    
        
    result_data = pd.DataFrame([{'label':label, 'score':score}], columns=['label', 'score'])
    
    return jsonify(result_data.to_json(orient="records")) 


@app.route('/predict-hypertension', methods=['POST'])
def predict_hypertension():

    paciente = request.get_json()
    
    print(paciente)

    # {"id": 1,  "nome": "joao",  "idade": 34,  "sexo": 0,  "peso": 84,  "altura": 170,  "bpm": 92,  "pressao": 146,  "respiracao": 11,  "temperatura": 37,  "glicemia": 128,  "saturacao_oxigenio": 98,  "estado_atividade": 2,  "dia_de_semana": 1,  "periodo_do_dia": 1,  "semana_do_mes": 2,  "estacao_do_ano": 3,  "passos": 303,  "calorias": 24.24,  "distancia": 378.75,  "tempo": 4.848,  "total_sleep_last_24": 6,  "deep_sleep_last_24": 5,  "light_sleep_last_24": 3,  "awake_last_24": 15,  "fumante": 1,  "genetica": 1,  "gestante": 0,  "frutas": 0,  "vegetais": 0,  "alcool": 1,  "doenca_coracao": 1,  "avc": 1,  "colesterol_alto": 1,  "exercicio": 0,  "timestampstr": "2022-03-20 11:19:28",  "timestamp_epoch": "1647775168"}

    data_teste = pd.DataFrame()
    data_teste['HighChol'] = [paciente["colesterol_alto"]]
    data_teste['BMI'] = [int(paciente["peso"] / ((paciente["altura"] / 100) ** 2))]
    data_teste['Smoker'] = [paciente["fumante"]] 
    data_teste['Stroke'] = [paciente["avc"]]
    data_teste['Drink_alcohol'] = [paciente["alcool"]]
    data_teste['Sex'] = [paciente["sexo"]]
    data_teste['Exercising'] = [paciente["exercicio"]]
    data_teste['Age'] = [paciente["idade"]]
    data_teste['Weight_kg'] = [paciente["idade"]]
    data_teste['Systolic_bp'] = [paciente["pressao"]]
    data_teste['Hemoglobin_concentration'] = [paciente["glicemia"]]
    data_teste['Congestive_heart_failure'] = [paciente["doenca_coracao"]]
    data_teste['Relative_heart_attack'] = [paciente["genetica"]]
    data_teste['Height_cm'] = [paciente["altura"]]    

    #realiza a predição.
    result = predict_model(HT_model, data=data_teste)

    #recupera os resultados.
    label = result["Label"][0]
    score = result["Score"][0]*100

    print(label)
    print(score)    
        
    result_data = pd.DataFrame([{'label':label, 'score':score}], columns=['label', 'score'])
    
    return jsonify(result_data.to_json(orient="records")) 


if __name__ == "__main__":
    app.run(debug=True, port = 5000, host='0.0.0.0')