import smbus2
import time
# TODO: implement logging rotations
# TODO: maybe the sht sensors can also work with gpiozero?


# time interval between measurements in seconds
measurement_interval = 60 * 1

# Define the I2C bus number and device address
bus = smbus2.SMBus(1)  # For Raspberry Pi 1 or 2, use 0 instead of 1
time.sleep(1)
address_30 = 0x44  # SHT sensor address (7-bit)

# SHT25 address, 0x40(64)
# Send temperature measurement command
# 0xF3(243)	NO HOLD master
i2c_address = 0x40


def read_sensor_sht30():  # Function to read temperature and humidity from the sensor
    # Send measurement command
    bus.write_i2c_block_data(address_30, 0x2C, [0x06])

    # Wait for measurement to complete
    time.sleep(0.5)

    # Read data (2 bytes for temperature, 2 bytes for humidity)
    data = bus.read_i2c_block_data(address_30, 0x00, 4)

    # Convert the data to temperature (in Celsius) and humidity (in %RH)
    temperature = (((data[0] * 256.0) + data[1]) * 175.72 / 65536.0) - 46.85
    humidity = (((data[2] * 256.0) + data[3]) * 125.0 / 65536.0) - 6.0

    return temperature, humidity


def read_sensor_sht25():
    # bus.write_byte(i2c_address, 0xF3)
    # SHT25 address, 0x40(64)
    # Read data back, 2 bytes
    # Temp MSB, Temp LSB
    data0 = bus.read_byte(i2c_address)
    data1 = bus.read_byte(i2c_address)

    # Convert the data
    temp = data0 * 256 + data1
    c_temp = -46.85 + ((temp * 175.72) / 65536.0)

    # SHT25 address, 0x40(64)
    # Send humidity measurement command
    # 0xF5(245)	NO HOLD master
    bus.write_byte(i2c_address, 0xF5)

    time.sleep(0.5)

    # SHT25 address, 0x40(64)
    # Read data back, 2 bytes
    # Humidity MSB, Humidity LSB
    data0 = bus.read_byte(i2c_address)
    data1 = bus.read_byte(i2c_address)

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
        pass
    elif temp < temp_threshold_min:
        pass
    # TODO: consider increasing measurement frequency if threshold not met


while True:
    print(f"Waiting for {measurement_interval}...")
    time.sleep(measurement_interval)
    print("Measuring...")
    temp_30, hum_30 = read_sensor_sht30()
    temp_25, hum_25 = read_sensor_sht25()
    # console output
    print(f"SHT30: Temp: {temp_30:.2f}°C Hum: {hum_30:.2f}%\n"
          f"SHT25: Temp: {temp_25:.2f}°C Hum: {hum_25:.2f}%\n")
    adjust_temp(temp_25)
