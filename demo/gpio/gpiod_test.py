import time
import gpiod

PIN_NO = 17
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(PIN_NO)
led_line.request(consumer="myLed", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        led_line.set_value(1)
        time.sleep(1)
        led_line.set_value(0)
        time.sleep(1)
finally:
    led_line.release()