from http import client
import requests
from datetime import datetime

def avg_temperature():
    data = open_sense_map_client()
    now_str = datetime.now().isoformat(timespec="milliseconds") + "Z"
    now_dt = datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    avg = []
    for sensor in data:
        #print(sensor)
        for key, val in sensor.items():
            sensor_time = sensor["updatedAt"]
            sensor_dt = datetime.strptime(sensor_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            if now_dt.hour - sensor_dt.hour <= 1:
                print("time deltia is less than 1 hour")
            else:
                print("time deltia is greater than 1 hour")




def open_sense_map_client():
    url = "https://api.opensensemap.org/boxes"
    # this bounding box roughly represents the continental US 
    args = {"bbox": "-125, 29, -101, 49"}

    with requests.Session() as session:
        response = session.get(url, params=args)
    response = response.json()
    #print(type(response))
    #for k, v in enumerate(response):
    #    print(k, v)
    return response

