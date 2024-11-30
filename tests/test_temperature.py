import pytest
import requests
import requests_mock
import json
from ..src.endpoints import temperature



def test_get_open_sense_boxes():
    with open('tests/mock_data.json', 'r') as file:
        data = json.load(file)
        session = requests.Session()
    
        with requests_mock.Mocker(session=session) as mock_session:
            mock_session.get('https://api.opensensemap.org/boxes', json=data)
            results = temperature.get_open_sense_boxes(session)

    # Verify type of results from function matches type of mocked data
    assert type(results) is type(data)

    # Verify length of results from function matches length of mocked data
    assert len(results) == len(data)

    # Verify contents of results from function matches contents of mocked data
    assert results == data


def test_recent_sense_boxes():
    with open('tests/mock_data.json', 'r') as file:
        data = list(json.load(file))
        results = temperature.recent_sense_boxes(data)
    
    # Verify return type of function 
    assert type(results) is list

    # Verify length of results based on mocked data
    assert len(results) == 9


# Verify an ID with a valid, recent temp measurement returns that measurement
def test_get_sense_box_temp_good():
    sb_id = "5ad4cf6d223bd8001939172d"
    with open(f'tests/mock_{sb_id}.json', 'r') as file:
        data = json.load(file)
        session = requests.Session()
    
        with requests_mock.Mocker(session=session) as mock_session:
            mock_session.get(f'https://api.opensensemap.org/boxes/{sb_id}', json=data)
            assert temperature.get_sense_box_temp(sb_id, session) == "20.40"


# Verify an ID with no recent temp measurement returns None
def test_get_sense_box_temp_bad():
    sb_id = "5ad4cfdc223bd80019392774"
    with open(f'tests/mock_{sb_id}.json', 'r') as file:
        data = json.load(file)
        session = requests.Session()
    
        with requests_mock.Mocker(session=session) as mock_session:
            mock_session.get(f'https://api.opensensemap.org/boxes/{sb_id}', json=data)
            assert temperature.get_sense_box_temp(sb_id, session) is None
