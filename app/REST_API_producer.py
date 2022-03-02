import requests
import json

try:
    # Data to be written 
    dictionary ={ 
    "id": 1, 
    "name": 2, 
    "bpm": 3
    } 
    url = "http://127.0.0.1:5000/kafka/pushToConsumers"
    # Serializing json  
    #json_object = json.dumps(dictionary).encode('utf-8')
    print(dictionary)
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