import requests
import json
import time
import random

try:
    
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
        url = "http://127.0.0.1:5000/kafka/pushToConsumers"
        headers = {'Content-type': 'application/vnd.kafka.json.v2+json'}
        response = requests.post(url, dictionary, headers)    
        response.raise_for_status()

        # Code here will only run if the request is successful
        print(response)    

except requests.exceptions.HTTPError as errh:
    print(errh)
except requests.exceptions.ConnectionError as errc:
    print(errc)
except requests.exceptions.Timeout as errt:
    print(errt)
except requests.exceptions.RequestException as err:
    print(err)





#curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
#      --data '{ "records": [ { "value": { "name": "testUser0" } }, { "value": { "name": "testUser1" } } ] }' \
#      "http://localhost:5000/kafka/pushToConsumer"    