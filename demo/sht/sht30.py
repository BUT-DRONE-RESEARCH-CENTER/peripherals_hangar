import smbus2
import time

# Define the I2C bus number and device address
bus = smbus2.SMBus(1)  # For Raspberry Pi 1 or 2, use 0 instead of 1
time.sleep(1)
address = 0x44  # SHT sensor address (7-bit)

# Function to read temperature and humidity from the sensor
def read_sensor():
    # Send measurement command
    bus.write_i2c_block_data(address, 0x2C, [0x06])

    # Wait for measurement to complete
    time.sleep(0.5)

    # Read data (2 bytes for temperature, 2 bytes for humidity)
    data = bus.read_i2c_block_data(address, 0x00, 4)

    # Convert the data to temperature (in Celsius) and humidity (in %RH)
    temperature = (((data[0] * 256.0) + data[1]) * 175.72 / 65536.0) - 46.85
    humidity = (((data[2] * 256.0) + data[3]) * 125.0 / 65536.0) - 6.0

    return temperature, humidity

# Main program
while True:
    temp, hum = read_sensor()
    print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temp, hum))
    time.sleep(2)  # Wait for 2 seconds before taking the next measurement
