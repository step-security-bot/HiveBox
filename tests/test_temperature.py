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