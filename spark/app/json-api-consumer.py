import requests
import json
import time


while True:
    try:
        url = "http://127.0.0.1:5000/getData"
            
        response = requests.get(url)
        response.raise_for_status()

        # Code here will only run if the request is successful
        print(response.json())  

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    time.sleep(2)


