import smbus2
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
from gpiozero import DigitalOutputDevice

# logger setup
LOG_DIR = "logs"
BACKUP_COUNT = 5  # Number of backup log files to keep
LOG_INTERVAL = 2  # Time interval in seconds for log rotation in iterations
MEASUREMENT_INTERVAL = 1  # time interval between measurements in seconds

# gpio output setup
PELTIER_PIN = 17
peltier_module = DigitalOutputDevice(PELTIER_PIN)

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
log_filename = os.path.join(LOG_DIR, datetime.now().strftime("%Y-%m-%d") + ".log")
handler = TimedRotatingFileHandler(
    filename=os.path.join(log_filename),
    when="midnight",  # Rotate log at midnight
    interval=2,  # Rotate every 1 interval (midnight in this case)
    backupCount=BACKUP_COUNT  # Keep only the last 5 log files
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


def read_sensor_sht30():  # Function to read temperature and humidity from the sensor
    try:
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

    except Exception as e:
        logger.error(f"Failed to read from SHT30 sensor: {e}")
        return None, None


def read_sensor_sht25():
    try:
        # Send temp measuring command
        bus.write_byte(ADDRESS_25, 0xE3)
        time.sleep(0.1)
        # Temp MSB, Temp LSB
        data0 = bus.read_byte(ADDRESS_25)
        data1 = bus.read_byte(ADDRESS_25)

        # Convert the data
        temp = data1 * 256 + data0
        c_temp = -46.85 + ((temp * 175.72) / 65536.0)

        # Send humidity measurement command
        bus.write_byte(ADDRESS_25, 0xE5)
        time.sleep(0.1)
        # Humidity MSB, Humidity LSB
        data0 = bus.read_byte(ADDRESS_25)
        data1 = bus.read_byte(ADDRESS_25)

        # Convert the data
        humidity = data0 * 256 + data1
        humidity = -6 + ((humidity * 125.0) / 65536.0)

        return c_temp, humidity

    except Exception as e:
        logger.error(f"Failed to read from SHT25 sensor: {e}")
        return None, None


def adjust_temp(temp, hum):
    """
    evaluates the best action to take based on inside hangar temp
    serves as a logical unit for the voltage supplied to peltier modules
    :param hum:
    :param temp: temperature inside hangar IN CELSIUS
    :return:
    """
    temp_threshold_max = 30  # TODO: invent better way, in which these variables are not read every time
    temp_threshold_min = 25  # TODO: also think about iterative referencing to this func
    if temp > temp_threshold_max:
        logger.warning(f"IN {temp:.2f}°C, {hum}%")
        peltier_cool()
    elif temp < temp_threshold_min:
        logger.warning(f"IN {temp:.2f}°C, {hum}%")
        peltier_warm()


def peltier_cool():
    peltier_temporary()


def peltier_warm():
    peltier_temporary()


def peltier_temporary():
    peltier_module.on()


iter_no = 1  # buffer
while True:
    temp_25, hum_25 = read_sensor_sht25()
    if temp_25 is None:
        logger.error("Failed to read from SHT25 sensor, retrying...")
        continue

    temp_30, hum_30 = read_sensor_sht30()
    if temp_30 is None:
        logger.error("Failed to read from SHT30 sensor, retrying...")
        continue

    if iter_no % LOG_INTERVAL == 0:  # Every LOG_INTERVALth iteration write data to log
        iter_no = 0  # Reset buffer
        logger.info(f"OUT {temp_30:.2f}°C, IN {temp_25:.2f}°C"
                    f"\tOUT{hum_30:.2f}%, IN {hum_25:.2f}%")
    
    adjust_temp(temp_25, hum_25)
    time.sleep(MEASUREMENT_INTERVAL)
    iter_no += 1
