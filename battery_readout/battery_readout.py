"""
This script utilizes smbus to communicate with PCF8591 in order to monitor battery state.
The battery has maximum voltage of 12.8V, there is a voltage divisor with 5M7 and 560k resistors.
"""
import smbus
import time

# define params
address = 0x48  # Address of PCF8591
bus = smbus.SMBus(1)
max_battery_voltage = 12.8  # in volts
r1 = 5.7e6  # in ohms
r2 = 560e3  # in ohms

while True:
    bus.write_byte(address,0x41)  # 0x41 is the address of A1in, the rest lays in the interval from 0x40 to 0x43, 0x48 is the address of PCF8591
    value = bus.read_byte(address)
    battery_percentage = value * 3.3 / 255 / max_battery_voltage * r2 / (r1 + r2)
    if battery_percentage > 1:
        battery_percentage = 1  # acount for fluctuations not to exceed 100%
    print("battery percentage: ", battery_percentage * 100, "%")
    time.sleep(0.1)
