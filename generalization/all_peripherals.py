"""
Author: Lukáš Lev, FEKT

script logic:
- script runs two separate theads for cameras and thermo-regulation
- according to the logic within each thread, the script will capture data and send it to the server
"""

import threading
import queue
import requests
import json
import subprocess

sht_queue = queue.Queue()
camera_queue = queue.Queue()


def run_thermoregulation(data_queue):
    subprocess.run(["python3", "electronics/peripherals/thermo_regulation/main.py"])  # TODO: adjust path


def run_camera(data_queue):
    subprocess.run(["python3", "electronics/peripherals/camera/camera.py"])


def post_to_server(flag, data):
    """
    Function to send data to the server.
    The server has to be prepared for recieving data from sht and camera separately
    (the way it has been done in this script: flag = 'sht' or 'camera', which then
    adjusts the URL to which the data is sent).

    NOTE: this function does not create live stream feed to the server, this has to
    be done yet (e.g. via a rpi streaming server). This task has been left to IT.

    :param flag:
    :param data:
    :return:
    """
    url = ''  # TODO: add server URL
    if flag == 'sht':
        url += 'sht'
        data = {
            "timestamp": data[0],
            "temperature_in": data[1],
            "humidity_in": data[2],
            "temperature_out": data[3],
            "humidity_out": data[4]
        }
    elif flag == 'cam':  # this only sends the previously recorded video, this is not live stream
        url += 'cam'
        data = {
            "timestamp": data[0],
            "video": data[1]
        }
    else:
        return -1

    response = requests.post(url, json=json.dumps(data))


# start script in a new thread
thread_sht = threading.Thread(target=run_thermoregulation, args=(sht_queue,))
thread_camera = threading.Thread(target=run_camera, args=(camera_queue,))
thread_sht.start()
thread_camera.start()


while True:
    try:
        data_sht = sht_queue.get(timeout=3)  # TODO: adjust timeout
        data_camera = camera_queue.get(timeout=3)  # TODO: adjust timeout

    except queue.Empty:
        print("No data available")
        continue
