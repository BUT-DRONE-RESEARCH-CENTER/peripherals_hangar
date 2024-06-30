from picamera2 import Picamera2
import time

def capture_image_from_camera(camera, output_filename):
    camera.start()
    time.sleep(2)  # Allow some time for the camera to warm up
    camera.capture_file(output_filename)
    camera.stop()

def main():
    # Initialize the first camera
    picam2_1 = Picamera2(camera_num=0)
    picam2_1_config = picam2_1.create_still_configuration()
    picam2_1.configure(picam2_1_config)

    # Initialize the second camera
    picam2_2 = Picamera2(camera_num=1)
    picam2_2_config = picam2_2.create_still_configuration()
    picam2_2.configure(picam2_2_config)

    # Capture images from both cameras
    capture_image_from_camera(picam2_1, "camera_1.jpg")
    capture_image_from_camera(picam2_2, "camera_2.jpg")

    print("Images captured and saved.")

if __name__ == "__main__":
    main()

