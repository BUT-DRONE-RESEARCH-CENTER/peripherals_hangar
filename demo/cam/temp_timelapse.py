import socket
import time
import os

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

# Specify the camera index (0 for the first camera, 1 for the second camera)
camera_index = 1  # Change to 1 if you want to use the second camera

picam2 = Picamera2(camera_index)
video_config = picam2.create_video_configuration({"size": (200, 200)})
video_config["controls"]["FrameRate"] = 1
picam2.configure(video_config)
encoder = H264Encoder(2000000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(("0.0.0.0", 10001))
    stream = sock.makefile("wb")

    output_net = FileOutput(stream)
    output_file = FfmpegOutput("timelapse.mp4")
    encoder.output = [output_file, output_net]

    picam2.start_encoder(encoder)
    picam2.start()
    time.sleep(10)
    print("File size after 10 sec: ", os.path.getsize(f"timelapse.mp4"))
    input("Waiting for interrupt...")
    picam2.stop_encoder()
    picam2.stop()
