# app.py

from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from subprocess import Popen

app = Flask(__name__)

@app.route('/execute', methods=['GET'])
def execute():

    print("Executing Command...")
    
    cmd = 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5,io.delta:delta-core_2.12:0.7.0 --master local[*] --driver-memory 12g --executor-memory 12g /home/jovyan/work/notebooks/event-producer.py'

    p = Popen(['watch', cmd]) # something long running
    
    #p.terminate()

    return jsonify({
        "message": "Command Executed OK", 
        "status": "Pass"})
    

if __name__ == "__main__":
    app.run(debug=True, port = 5000, host='0.0.0.0')