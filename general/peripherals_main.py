"""
Author: Lukáš Lev, FEKT

script logic:
- script runs two separate theads for cameras and thermo-regulation
- according to the logic within each thread, the script will capture data and send it to the server

TODO:
- get the correct server urls
- implement video live feed to the server (so far cameras do not send anything to the server)
- create option for full hangar or just landing pad - dedicate gpio pins for this
"""

import threading
import queue
import requests
import json
import subprocess
import argparse

sht_queue = queue.Queue()
camera_queue = queue.Queue()


def run_thermoregulation(data_queue):
    subprocess.run(["python3", "sht.py"])


def run_camera(data_queue):
    subprocess.run(["python3", "cam.py"])


def run_camera_lp(data_queue):
    subprocess.run(["python3", "cam_lp.py"])


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

    response = requests.post(url, json=data)


def arg_recognition():
    parser = argparse.ArgumentParser(description="If argument -lp is present, "
                                                 "the script will only record the landing pad")
    parser.add_argument("-lp", "--landing_pad", action="store_true", help="Record only the landing pad")
    args = parser.parse_args()  # parse the arguments
    return args


def main():
    arguments = arg_recognition()  # get the arguments

    if not arguments.landing_pad:
        # start script in a new thread
        thread_sht = threading.Thread(target=run_thermoregulation, args=(sht_queue,))
        thread_camera = threading.Thread(target=run_camera, args=(camera_queue,))
        thread_sht.start()
        thread_camera.start()
    else:
        thread_camera_lp = threading.Thread(target=run_camera_lp, args=(camera_queue,))
        thread_camera_lp.start()

    while True:  # main loop
        try:
            data_sht = sht_queue.get(timeout=5)  # TODO: adjust timeout
            data_camera = camera_queue.get(timeout=3)  # TODO: adjust timeout

        except queue.Empty:
            print("No data available")
            continue


if __name__ == "__main__":
    __import__("subprocess").Popen(["python3", "advertise.py"], stdout=None, stderr=None, stdin=None, close_fds=True, start_new_session=True) # keď boh dá tak pôjde
    main()
