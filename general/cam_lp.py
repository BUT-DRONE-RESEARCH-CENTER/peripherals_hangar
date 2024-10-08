"""
camera_1 according to the README.md, this camera is inside
"""

import logging
import os
import socket
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

# Constants
VID_DIR = "vids"  # name of the directory in which recorded videos are stored
BACKUP_COUNT = 8  # how many videos will be preserved before rotation
MAX_FILE_SIZE = 1024 * 1024 * 200  # maximum file size of one video
FPS_IN = 5  # FPS for camera inside of the hangar

# Setup logging
logger = logging.getLogger("camera_logger")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler("camera.log", when="midnight", backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Ensure output directory exists
os.makedirs(VID_DIR, exist_ok=True)

# Picamera setup
picam2_1 = Picamera2(camera_num=1)

video_config_1 = picam2_1.create_video_configuration({"size": (200, 200)})

video_config_1["controls"]["FrameRate"] = FPS_IN

picam2_1.configure(video_config_1)

encoder_1 = H264Encoder(2000000)


# Define functions
def file_too_big(file_path, max_size=MAX_FILE_SIZE):
    if os.path.exists(file_path) and os.path.getsize(file_path) >= max_size:
        logger.info("Previous record removed due to size limit.")
        remove_oldest_rec()
        return True
    return False


def remove_oldest_rec():
    dir_list = sorted(os.listdir(VID_DIR))
    if len(dir_list) >= BACKUP_COUNT:
        oldest_file = os.path.join(VID_DIR, dir_list[0])
        os.remove(oldest_file)
        logger.info(f"Removed oldest file: {oldest_file}")


def get_timestamped_filename(prefix="record"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(VID_DIR, f"{prefix}_{timestamp}.h264")


# Main loop
def main():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_0, socket.socket(socket.AF_INET,
                                                                                       socket.SOCK_DGRAM) as sock_1:
            sock_1.connect(("0.0.0.0", 10002))

            stream_1 = sock_1.makefile("wb")

            output_net_1 = FileOutput(stream_1)

            output_file_path_1 = get_timestamped_filename("doors_record")
            output_file_1 = FfmpegOutput(output_file_path_1)
            encoder_1.output = [output_file_1, output_net_1]

            picam2_1.start_encoder(encoder_1)

            try:
                while True:
                    picam2_1.start()
                    if file_too_big(output_file_path_1, max_size=MAX_FILE_SIZE * 10):
                        picam2_1.stop_recording()
                    time.sleep(1)
            except Exception as e:
                logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
