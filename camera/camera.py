import logging
from logging.handlers import TimedRotatingFileHandler
import os

import socket
import time
from datetime import datetime

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

# setup
VID_DIR = "vids"
BACKUP_COUNT = 3  # number of backup files to keep
MAX_FILE_SIZE = 1024 * 1024 * 5  # maximum file size in bytes
FPS = 2  # TODO: yet to be implemented

# picam setup
picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (400, 300)})
video_config["controls"]["FrameRate"] = FPS
picam2.configure(video_config)
encoder = H264Encoder(2000000)

# define functions
def file_too_big(file_path):  # TODO: check if this approach is correct, otherwise use max time
    if os.path.exists(file_path) and os.path.getsize(file_path) >= MAX_FILE_SIZE:
        print("Previous record removed")
        remove_oldest_rec()
        return True
    return False

def remove_oldest_rec():
    dir_list = sorted(os.listdir(VID_DIR))
    if len(dir_list) >= BACKUP_COUNT:
        oldest_file = os.path.join(VID_DIR, dir_list[0])
        os.remove(oldest_file)

# ensure output dir exists
if not os.path.exists(VID_DIR):
    os.mkdir(VID_DIR)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("0.0.0.0", 10001))
        stream = sock.makefile("wb")

        output_net = FileOutput(stream)
        output_file_path = get_timestamped_filename()
        output_file = FfmpegOutput(output_file_path)
        encoder.output = [output_file, output_net]

        picam2.start_encoder(encoder)
        picam2.start()
        while True:
            if file_too_big(output_file_path):
                picam2.stop_recording()
                break
            time.sleep(1)
