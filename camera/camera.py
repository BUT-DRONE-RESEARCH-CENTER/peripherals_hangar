"""
camera_0 according to the README.md, this camera is outside
camera_1 according to the README.md, this camera is inside
"""

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
BACKUP_COUNT = 5  # number of backup files to keep
MAX_FILE_SIZE = 1024 * 1024 * 200  # maximum file size in bytes
FPS = 1

# picam setup
picam2_0 = Picamera2(camera_num=0)
picam2_1 = Picamera2(camera_num=1)
video_config_0 = picam2_0.create_video_configuration({"size": (200, 200)})
video_config_1 = picam2_1.create_video_configuration({"size": (200, 200)})
video_config_0["controls"]["FrameRate"] = FPS
video_config_1["controls"]["FrameRate"] = FPS
picam2_0.configure(video_config_0)
picam2_1.configure(video_config_1)
encoder = H264Encoder(2000000)


# define functions
def file_too_big(file_path):
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


def get_timestamped_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(VID_DIR, f"record_{timestamp}.h264")


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
