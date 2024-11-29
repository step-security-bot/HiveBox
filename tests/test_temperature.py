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

    # Do not return these results; mock them again for testing other methods in temperature
    #return results

def test_recent_sense_boxes():
    with open('tests/mock_data.json', 'r') as file:
        data = list(json.load(file))
        results = temperature.recent_sense_boxes(data)
    
    assert type(results) is list
    assert len(results) == 9


def test_get_sense_box_temp(sb_id):
    with open(f'tests/mock_{sb_id}.json', 'r') as file:
        data = json.load(file)
        session = requests.Session()
    
        with requests_mock.Mocker(session=session) as mock_session:
            mock_session.get(f'https://api.opensensemap.org/boxes/{sb_id}', json=data)
            results = temperature.get_sense_box_temp(sb_id, session)

        return results
    
assert test_get_sense_box_temp("5ad4cf6d223bd8001939172d") == "20.40"
assert test_get_sense_box_temp("5ad4cfdc223bd80019392774") is None