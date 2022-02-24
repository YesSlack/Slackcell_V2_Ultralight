import pytest
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.streamer import DataStreamer
from src.loadcell import LoadCell


@pytest.fixture
def lc():
    streamer = DataStreamer()
    return LoadCell(streamer)


def test_print(lc):
    print(lc)


def test_start(lc):
    lc.start()
    time.sleep(0.1)
    # assert lc is running
    assert lc.force != 0
    assert lc.max_force != -62000
    assert lc.min_force != 62000
    assert lc.hx is not None

    lc.stop_thread = True
    time.sleep(0.1)
    assert lc.running is False


def test_recording(lc):
    lc.set_save_path(os.path.join('tests', 'static', 'data'))
    response = lc.start_recording()
    assert response == (True, True)
    time.sleep(0.1)
    response = lc.start_recording()
    assert response == (False, True)
    response = lc.stop_recording()
    assert response == (True, False)
    assert lc.recording is False
    response = lc.stop_recording()
    assert response == (False, False)
    with open(lc.csv_path) as file:
        csv = file.readlines()
    assert csv[0] == "timestamp,force\n"
    assert len(csv) > 2
    lc.stop_thread = True
    time.sleep(0.1)
