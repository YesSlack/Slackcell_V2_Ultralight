import os
import random
import gpiozero
import platform
import json
import threading
import time

from flask import Flask, render_template, request, Response, jsonify

PI = platform.uname()[4].startswith("arm")


def create_app(streamer, lc):
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    @app.route("/")
    def index():
        return render_template('index.html', pi=PI, list_csv=os.listdir(lc.save_path))

    @app.route('/listen', methods=['GET'])
    def listen():
        print("Added listener ", request.remote_addr)

        def stream():
            messages = streamer.listen()  # returns a queue.Queue

            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield msg

        return Response(stream(), mimetype='text/event-stream')

    @app.route("/calibration")
    def calibration():
        lc.stop_thread = True
        return render_template('calibration.html')

    @app.route("/estimate_offset")
    def api_estimate_offset():
        return str(lc.estimate_offset())

    @app.route("/estimate_reference_unit/<int:known_force>")
    def api_estimate_reference_unit(known_force):
        return str(round(lc.estimate_reference_unit(known_force)))

    @app.route("/save_hx_config/<int:offset>/<int:reference_unit>")
    def api_save_hx_config(offset, reference_unit):
        lc.save_config(offset, reference_unit)
        return f"Saved: Offset = {offset}, Reference Unit = {reference_unit}"

    @app.route("/max_force")
    def api_max_force():
        return str(lc.max_force)

    @app.route("/reset_max_force")
    def api_reset_max_force():
        lc.max_force = -60000
        print("Max force resetted.")
        return str(lc.max_force)

    @app.route("/force")
    def api_force():
        if lc.stop_thread:
            lc.start()
        return str(lc.force)

    @app.route("/record_start")
    def api_record_start():
        return jsonify(lc.start_recording())

    @app.route("/record_stop")
    def api_record_stop():
        return jsonify(lc.stop_recording(), lc.csv_path.replace(lc.save_path + os.sep, ""))

    @app.route("/reference_unit")
    def api_reference_unit():
        return str(lc.hx.get_reference_unit())

    @app.route("/offset")
    def api_offset():
        return str(lc.hx.get_offset())

    @app.route("/pi_temp")
    def api_pi_temp():
        return get_pi_temp()

    @app.route("/pi_load")
    def api_pi_load():
        return get_pi_load()

    @app.route("/pi_disk")
    def api_pi_disk():
        return get_pi_disk()

    @app.route("/pi_stats")
    def api_pi_stats():
        return {'pi_temp': get_pi_temp(),
                'pi_load': get_pi_load(),
                'pi_disk': get_pi_disk()}

    thread = threading.Thread(target=pi_stats, args=(streamer,))
    thread.start()

    return app


def get_pi_temp():
    if PI:
        return f"{gpiozero.CPUTemperature().temperature:.1f}"  # pragma: no cover
    else:
        return str(random.randint(300, 800) / 10)


def get_pi_load():
    if PI:
        return f"{gpiozero.LoadAverage(minutes=1).load_average * 100:.1f}"  # pragma: no cover
    else:
        return str(random.randint(10, 1000) / 10)


def get_pi_disk():
    if PI:
        return f"{gpiozero.DiskUsage().usage:.1f}"  # pragma: no cover
    else:
        return str(random.randint(100, 400) / 10)


def pi_stats(streamer):
    while True:
        stats = {
            'pi_temp': get_pi_temp(),
            'pi_load': get_pi_load(),
            'pi_disk': get_pi_disk()
        }
        time.sleep(30)
        streamer.stream(event="pi_stats", data=json.dumps(stats))
