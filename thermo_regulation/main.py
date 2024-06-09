import smbus2
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
# TODO: maybe the sht sensors can also work with gpiozero?

# logger setup
LOG_FILE = "therm_reg.log"
LOG_DIR = "logs"
BACKUP_COUNT = 5  # Number of backup log files to keep
LOG_INTERVAL = 2  # Time interval in seconds for log rotation in iterations
MEASUREMENT_INTERVAL = 1  # time interval between measurements in seconds

# ensure log dir exists
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# Logger setup
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

# Define the I2C bus number and device address
bus = smbus2.SMBus(1)  # For Raspberry Pi 1 or 2, use 0 instead of 1
time.sleep(1)  # sleep after initializing smbus

ADDRESS_30 = 0x44  # SHT30 sensor address (7-bit)
ADDRESS_25 = 0x40  # SHT25 address, 0x40(64) 0xF3(243)	NO HOLD master

# Logger setup
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

# Timed rotating file handler
handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    when="midnight",  # Rotate log at midnight
    interval=2,  # Rotate every 1 interval (midnight in this case)
    backupCount=BACKUP_COUNT  # Keep only the last 5 log files
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


def read_sensor_sht30():  # Function to read temperature and humidity from the sensor
    # Send measurement command
    bus.write_i2c_block_data(ADDRESS_30, 0x2C, [0x06])

    # Wait for measurement to complete
    time.sleep(0.5)

    # Read data (2 bytes for temperature, 2 bytes for humidity)
    data = bus.read_i2c_block_data(ADDRESS_30, 0x00, 4)

    # Convert the data to temperature (in Celsius) and humidity (in %RH)
    temperature = (((data[0] * 256.0) + data[1]) * 175.72 / 65536.0) - 46.85
    humidity = (((data[2] * 256.0) + data[3]) * 125.0 / 65536.0) - 6.0

    return temperature, humidity


def read_sensor_sht25():  # TODO: fix unexpected output
    # Send temp measuring command
    bus.write_byte(ADDRESS_25, 0xF3)
    time.sleep(0.5)
    # Temp MSB, Temp LSB
    data0 = bus.read_byte(ADDRESS_25)
    data1 = bus.read_byte(ADDRESS_25)

    # Convert the data
    temp = data0 * 256 + data1
    c_temp = -46.85 + ((temp * 175.72) / 65536.0)

    # Send humidity measurement command
    bus.write_byte(ADDRESS_25, 0xF5)
    time.sleep(0.5)
    # Humidity MSB, Humidity LSB
    data0 = bus.read_byte(ADDRESS_25)
    data1 = bus.read_byte(ADDRESS_25)

    # Convert the data
    humidity = data0 * 256 + data1
    humidity = -6 + ((humidity * 125.0) / 65536.0)

    return c_temp, humidity


def adjust_temp(temp):
    """
    evaluates the best action to take based on inside hangar temp
    serves as a logical unit for the voltage supplied to peltier modules
    :param temp: temperature inside hangar IN CELSIUS
    :return:
    """
    temp_threshold_max = 35
    temp_threshold_min = 5
    if temp > temp_threshold_max:
        logger.warning(f"OUT {temp_30}\tIN {temp_25}")
    elif temp < temp_threshold_min:
        logger.warning(f"OUT {temp_30}\tIN {temp_25}")  # TODO: 


iter_no = 1  # buffer
while True:
    temp_25, hum_25 = read_sensor_sht25()
    time.sleep(5)
    temp_30, hum_30 = read_sensor_sht30()
    if iter_no % LOG_INTERVAL == 0:  # every LOG_INTERVALth iteration write data to log
        iter_no = 0  # reset buffer
        logger.info(f"OUT {temp_30}\tIN {temp_25}")
    adjust_temp(temp_25)
    time.sleep(MEASUREMENT_INTERVAL)
    iter_no += 1
