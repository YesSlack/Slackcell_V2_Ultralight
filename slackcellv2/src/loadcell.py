import time
import sys
# import traceback
import os
import threading
import configparser
from collections import deque
from datetime import datetime


class LoadCell:
    """
    Class for a load cell with HX711 ADC
    """

    def __init__(self, streamer, config_name='slackcell.cfg'):
        self.config = configparser.ConfigParser()
        self.config_name = config_name
        self.config.read(config_name)
        self.streamer = streamer
        self.force = 0
        self.min_force = 62000
        self.max_force = -62000
        self.force_dq = deque(maxlen=5)
        self.thread = None
        self.recording = False
        self.save_path = None
        self.set_save_path(os.path.join("src", "static", "data"))
        self.csv_path = ""
        self.stop_thread = False
        self.sleep = 1
        self.raw_filter_values = []
        self.filter_values = []
        self.hx = None
        self.timestamp = time.time()
        self.running = False
        self.strip = None
        self.setup()

    def setup(self):
        """
        Reading values from config
        :return:
        """
        self.sleep = self.config['HX711'].getint('SLEEP')
        self.raw_filter_values = [int(x) for x in self.config['HX711']
                                  .get('RAW_FILTER_VALUES').split(',')]
        self.filter_values = []
        self.setup_hx711()

    def setup_hx711(self):
        """
        Reading HX711 config data
        :return:
        """
        print("Initializing HX711")
        if not self.config['HX711'].getboolean('EMULATE'):
            from src.hx711py.hx711 import HX711     # pragma: no cover
        else:
            from src.hx711py.emulated_hx711 import HX711
        self.hx = HX711(self.config['PINS'].getint('DOUT'), self.config['PINS'].getint('CLK'))
        self.hx.reset()
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_offset(self.config['HX711'].getint('OFFSET'))
        self.hx.set_reference_unit(self.config['HX711'].getint('REFERENCE_UNIT'))
        self.set_filter_values()
        self.hx.reset()

    def set_save_path(self, path):
        os.makedirs(path, exist_ok=True)
        self.save_path = path

    def __str__(self):
        """
        Printing load cell settings
        :return:
        """
        return f"""Offset: {self.hx.get_offset()}
Reference Unit: {self.hx.get_reference_unit()}
Save Path: {self.save_path}
Min Force: {self.min_force}
Max Force: {self.max_force}
Sleep:     {self.sleep}
Raw Filter Values: {self.filter_values}
"""

    def loop(self):
        start_time = time.time()
        prev_time = start_time
        cnt = 0
        while True:
            # HX711 in 80Hz mode should be able to read every 12.5ms
            if self.hx.is_ready():
                self.timestamp = time.time()
                force = int(self.hx.get_weight(1))
                # print(f"\nTimedelta: {(self.timestamp-prev_time)}")
                # print(f"Force: {self.force} [N]")
                # if force not in self.filter_values:
                try:
                    force = self.filter_force(force)
                    self.update_force(force)
                    if self.force == self.max_force:
                        self.streamer.stream(event="max_force", data=self.max_force)
                    if self.recording:
                        self.write_line_csv()
                    if cnt == 4:
                        self.streamer.stream(data=f"{self.timestamp},{self.force},{self.timestamp - prev_time}")
                        cnt = 0
                    cnt += 1
                except ValueError:
                    print(f"Ignored value: {force}")
                    # else:
                    #     print(f"Filtered Force deviation: {force} [N]")
                # else:
                #     print(f"Filtered Force discrete: {force} [N]")
                prev_time = self.timestamp
                # reduce load on cpu
                time.sleep(self.sleep / 1000)
            if self.stop_thread:
                self.running = False
                print("Stopped loadcell thread.")
                break

    def update_force(self, _force):
        self.force = _force
        # update extrema
        self.max_force = max(self.max_force, self.force)
        self.min_force = min(self.min_force, self.force)

    def filter_force(self, _force):
        if _force in self.filter_values:
            raise ValueError
        self.force_dq.append(_force)
        if len(self.force_dq) > 2:
            lst = list(self.force_dq)
            _force = round((sum(lst) - min(lst) - max(lst)) / (len(self.force_dq) - 2))
        return _force

    def start(self):
        self.stop_thread = False
        print("Start thread of load cell.")
        self.thread = threading.Thread(target=self.loop, args=())
        self.running = True
        try:
            self.thread.start()
        except KeyboardInterrupt:
            # if not self.config['HX711'].getboolean('EMULATE'):
            #     GPIO.cleanup()      # pragma: no cover
            # traceback.print_exc()
            sys.exit()

    def start_recording(self):
        if not self.running:
            self.start()
        if self.recording:
            print(f"Warning: Loadcell is already recording in {self.csv_path}."
                  "Data gets appended to file.")
            return False, self.recording
        else:
            self.csv_path = os.path.join(
                self.save_path, datetime.now().strftime('slackcell_%Y-%m-%d_%H%M%S.csv'))
            csv = open(self.csv_path, "w")
            csv.write("timestamp,force\n")
            csv.close()
            print(f"Loadcell starts recording in {self.csv_path}.")
            self.recording = True
            return True, self.recording

    def stop_recording(self):
        if self.recording:
            self.recording = False
            print(f"Loadcell stopped recording in {self.csv_path}.")
            return True, self.recording
        else:
            print("Warning: Loadcell was not recording.")
            return False, self.recording

    def write_line_csv(self):
        csv = open(self.csv_path, "a")
        csv.write(f"{datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')},{self.force}\n")
        csv.close()

    def estimate_offset(self):
        self.stop_thread = True
        time.sleep(0.1)
        print("Reading forces for offset estimation.")
        val = round(self.hx.tare(800))
        self.hx.set_offset(val)
        print("New offset: ", val)
        return val

    def estimate_reference_unit(self, known_force):
        self.stop_thread = True
        time.sleep(0.1)
        print("Reading forces for reference unit estimation.")
        return (self.hx.read_average(800) - self.hx.get_offset()) / known_force

    def save_config(self, offset, reference_unit):
        self.hx.set_offset(offset)
        self.hx.set_reference_unit(reference_unit)
        self.set_filter_values()
        self.config['HX711']['REFERENCE_UNIT'] = str(self.hx.get_reference_unit())
        self.config['HX711']['OFFSET'] = str(self.hx.get_offset())
        with open(self.config_name, 'w') as configfile:
            self.config.write(configfile)

    def set_filter_values(self):
        self.filter_values = [int((x - self.hx.get_offset())
                              / self.hx.get_reference_unit()) for x in self.raw_filter_values]
