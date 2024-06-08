import logging
from logging.handlers import TimedRotatingFileHandler
import os

# setup
VID_DIR = "vids"
VID_FILE = "record.h264"
BACKUP_COUNT = 3  # number of backup files to keep
FPS = 2

# define functions
def get_file_size(file_path):
    pass

# ensure output dir exists
if not os.path.exists(VID_DIR):
    os.mkdir(VID_DIR)


