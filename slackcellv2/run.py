import shutil
import os

from src.streamer import DataStreamer
from src.loadcell import LoadCell
from src.app import create_app

LIVEDATA = True

if __name__ == "__main__":
    # change working dir path of run.py
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    # copy default config
    config_name = "slackcell.cfg"
    if not os.path.isfile(config_name):
        shutil.copy("example.cfg", config_name)
    # start all slackcell parts
    streamer = DataStreamer()
    lc = LoadCell(streamer)
    print(lc)
    if LIVEDATA:
        lc.start()
    app = create_app(streamer, lc)
    app.run(host='0.0.0.0', port=8800, debug=not LIVEDATA, use_reloader=not LIVEDATA)
