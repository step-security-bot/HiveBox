import asyncio
import requests
from datetime import datetime
from time import perf_counter
import json

# avg time without sessions: 8.5 best 5 worst 32
# avg time with sessions: 2.2 best 1.8 worst 2.4
# avg time with asyncio: 1.1


async def avg_temperature():
    """
    Returns the average temperatures in Celcius for sense boxes which have a valid temperature measurement.

    Parameters: None

    """
    start = perf_counter()
    with requests.Session() as session:
        sb_ids = get_open_sense_boxes(session)
        sb_ids = recent_sense_boxes(sb_ids)

        results = await get_all_sense_box_temps(sb_ids, session)
        stop = perf_counter()
        print(f"total time taken {stop - start} seconds")
        avg = sum(results) / len(results)
        return round(avg, 3)


async def get_all_sense_box_temps(sb_ids: list, session):
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(None, get_sense_box_temp, sb_id, session) for sb_id in sb_ids
    ]

    results = await asyncio.gather(*futures)
    # filter out null results
    return [float(result) for result in results if result is not None]


def get_sense_box_temp(sb_id: str, session):
    """
    Returns the temperature for a given sense box ID.

    Parameters: ID of the sense box

    """
    url = "https://api.opensensemap.org/boxes/"
    start = perf_counter()

    response = session.get(url + sb_id)
    response = response.json()

    # Loop over sensors list in the response
    for sensor in response["sensors"]:
        # if "temp" is in the title of the sensor, we can assume it is measuring temperature. We also check that the lastMeasurement exists so we don't collect NoneType results
        if "temp" in sensor["title"].casefold() and sensor["lastMeasurement"]:
            stop = perf_counter()
            print(f"Api call for sb_id {sb_id} took {stop - start} seconds")
            return sensor["lastMeasurement"]["value"]



def recent_sense_boxes(sense_boxes: list):
    """
    Returns a list of sense box IDs, for sense boxes that have an updatedAt property of less than or equal to 1 hour

    Parameters: sense_boxes: a list of dicts

    """
    recent_boxes = []
    start = perf_counter()

    now_str = datetime.now().isoformat(timespec="milliseconds") + "Z"
    now_dt = datetime.strptime(now_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    for sense_box in sense_boxes:
        sensor_time = sense_box["updatedAt"]
        sensor_dt = datetime.strptime(sensor_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if now_dt.hour - sensor_dt.hour <= 1:
            recent_boxes.append(sense_box["_id"])
    stop = perf_counter()
    print(f"filtering results took {stop - start} seconds")
    print(recent_boxes)
    return recent_boxes


def get_open_sense_boxes(session):
    """
    Returns a list of sense boxes within the specified bounding box

    Parameters: None

    """
    url = "https://api.opensensemap.org/boxes"
    # this bounding box roughly represents WA state
    args = {"bbox": "-124,47,-121,49"}

    start = perf_counter()

    response = session.get(url, params=args)
    response = response.json()
    stop = perf_counter()
    print(f"Intial API call took {stop - start} seconds")

    return response
