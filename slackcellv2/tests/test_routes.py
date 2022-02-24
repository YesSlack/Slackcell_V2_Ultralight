import pytest
import sys
from os import path
import random
import json
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.app import create_app
from src.streamer import DataStreamer
from src.loadcell import LoadCell


@pytest.fixture
def client():
    streamer = DataStreamer()
    lc = LoadCell(streamer)
    with create_app(streamer, lc).test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_calibration(client):
    response = client.get('/calibration')
    assert response.status_code == 200

    response = client.get('/offset')
    assert response.status_code == 200
    offset = response.data

    response = client.get('/reference_unit')
    assert response.status_code == 200
    reference_unit = response.data

    offset_test = 200
    reference_unit_test = 100
    response = client.get(f'/save_hx_config/{str(offset_test)}/{reference_unit_test}')
    assert response.status_code == 200
    assert response.data == f"Saved: Offset = {offset_test}, Reference Unit = {reference_unit_test}".encode('ascii')

    response = client.get('/offset')
    assert response.data == str(offset_test).encode()
    response = client.get('/reference_unit')
    assert response.data == str(reference_unit_test).encode()

    # reset config data
    response = client.get(f'/save_hx_config/{offset.decode()}/{reference_unit.decode()}')
    assert response.status_code == 200


def test_hx_estimates(client):
    response = client.get('/estimate_offset')
    assert response.status_code == 200
    response = client.get('/estimate_reference_unit/500')
    assert response.status_code == 200


# def test_listen(client):
#     response = client.get('/listen')
#     assert response.status_code == 200
#     assert response.mimetype == "text/event-stream"


def test_pi_stats(client):
    random.seed(5)
    response = client.get('/pi_stats')
    assert response.status_code == 200
    assert response.data == b'{"pi_disk":"28.3","pi_load":"27.1","pi_temp":"61.8"}\n'

    response = client.get('/pi_temp')
    assert response.status_code == 200
    assert response.data == b'70.7'

    response = client.get('/pi_disk')
    assert response.status_code == 200
    assert response.data == b'37.1'

    response = client.get('/pi_load')
    assert response.status_code == 200
    assert response.data == b'3.9'


def test_recording(client):
    response = client.get('/record_start')
    assert response.status_code == 200
    assert response.data == b'[true,true]\n'

    response = client.get('/record_stop')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf8').replace("'", '"'))
    assert data[0] == [True, False]
    assert data[1].find('.csv') != -1

    # stop the started lc thread again
    response = client.get('/calibration')


def test_forces(client):
    response = client.get('/force')
    assert response.status_code == 200
    assert response.data == b'0'

    response = client.get('/max_force')
    assert response.status_code == 200
    assert response.data == b'-62000'

    response = client.get('/reset_max_force')
    assert response.status_code == 200
    assert response.data == b'-60000'
