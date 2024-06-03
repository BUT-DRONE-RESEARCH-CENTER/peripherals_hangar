from gpiozero import DigitalOutputDevice
from time import sleep

output_pin = 17

output_device = DigitalOutputDevice(output_pin)

while True:
    output_device.on()
    sleep(0.5)
    output_device.off()
    sleep(1)
