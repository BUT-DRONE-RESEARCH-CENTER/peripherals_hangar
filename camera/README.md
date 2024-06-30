# Cameras
# Useful terminal commands
- list active cameras: _libcamera-still --list-cameras_
- take a picture:
  - The first argument is the name of the output file, second is the camera, third we set a five-second delay (5000 ms) to give us time to frame the shot.
  - _libcamera-jpeg -o cam0.jpg –camera 0 -t 5000_
