from http import client
import requests
from datetime import datetime

# todo:
# remove the double call to the api from get_open_sense_boxes
# time with and without sessions
# see if parallelizing individual sensebox calls speeds up even more

def avg_temperature():
    with requests.Session() as session:
        result = []
        ids = get_open_sense_boxes(session)
        ids = recent_sense_boxes(ids, session)
        #ids = ["5ad4cf6d223bd8001939172d", "5ad4cfdc223bd80019392774"]
        for id in ids:
            temp = get_sense_box_temp(id, session)
            if temp is not None:
                result.append(temp)
        print(result)
        return result




def get_sense_box_temp(id: str, session):
    ''' 
    Returns the temperature for a given sense box ID.

    Parameters: ID of the sense box
    
    '''
    
    url = "https://api.opensensemap.org/boxes/"
    # temporary ID
    #id = "5ad4cf6d223bd8001939172d"

    #with requests.Session() as session:
    response = session.get(url + id)
    response = response.json()
    # Loop over sensors list in the response
    for sensor in response["sensors"]:
        # if "temp" is in the title of the sensor, we can assume it is measuring temperature. We also check that the lastMeasurement exists so we don't collect NoneType results
        if "temp" in sensor["title"].casefold() and sensor["lastMeasurement"]:
            return sensor["lastMeasurement"]["value"]


def recent_sense_boxes(sense_boxes: dict, session):
    ''' 
    Returns a list of sense box IDs, for sense boxes that have an updatedAt property of less than or equal to 1 hour

    Parameters: None
    
    '''
    sense_boxes = get_open_sense_boxes(session)
    recent_boxes = []

    now_str = datetime.now().isoformat(timespec="milliseconds") + "Z"
    now_dt = datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    for sense_box in sense_boxes:

        sensor_time = sense_box["updatedAt"]
        sensor_dt = datetime.strptime(sensor_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if now_dt.hour - sensor_dt.hour <= 1:
            recent_boxes.append(sense_box["_id"])

    return recent_boxes


def get_open_sense_boxes(session):
    ''' 
    Returns a dict of sense boxes within the specified bounding box

    Parameters: None
    
    '''
    url = "https://api.opensensemap.org/boxes"
    # this bounding box roughly represents WA state
    args = {"bbox": "-124,47,-121,49"}

    #with requests.Session() as session:
    print("running get_open_sense_boxes")
    response = session.get(url, params=args)
    response = response.json()

    return response

