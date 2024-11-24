from http import client
import requests
from datetime import datetime

def get_sense_box_temp():
    ''' 
    Returns the temperature for a given sense box ID.

    Parameters: Temperature for the sense box
    
    '''
    
    url = "https://api.opensensemap.org/boxes/"
    # temporary ID
    id = "5ad4cf6d223bd8001939172d"

    with requests.Session() as session:
        response = session.get(url + id)
    response = response.json()

    return response





def recent_sense_boxes():
    ''' 
    Returns a list of sense box IDs, for sense boxes that have an updatedAt property of less than or equal to 1 hour

    Parameters: None
    
    '''
    data = get_open_sense_boxes()
    recent_boxes = []

    now_str = datetime.now().isoformat(timespec="milliseconds") + "Z"
    now_dt = datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    for sense_box in data:

        sensor_time = sense_box["updatedAt"]
        sensor_dt = datetime.strptime(sensor_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if now_dt.hour - sensor_dt.hour <= 1:
            recent_boxes.append(sense_box["_id"])

    return recent_boxes




def get_open_sense_boxes():
    ''' 
    Returns a dict of sense boxes within the specified bounding box

    Parameters: None
    
    '''
    url = "https://api.opensensemap.org/boxes"
    # this bounding box roughly represents WA state
    args = {"bbox": "-124,47,-121,49"}

    with requests.Session() as session:
        response = session.get(url, params=args)
    response = response.json()

    return response

