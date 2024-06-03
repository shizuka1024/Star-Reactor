from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep
import random

CS_PIN = 8  # Replace with your actual CS pin
BLOCK_NUM = 1  # Replace with your block number

HEIGHT = 8
WIDTH = 8 * BLOCK_NUM

# Define SPI interface
serial = spi(port=0, device=0, gpio=noop(), cs=CS_PIN)

# Define LED matrix device
device = max7219(serial, cascaded=BLOCK_NUM, block_orientation=-90)

def clear_display():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="black", fill="black")
    sleep(1)

def light_pixels_for_number(number):
    with canvas(device) as draw:
        if number == 1:
            pixels = [(0, 6), (0, 7), (1, 6), (1, 7)]
        elif number == 2:
            pixels = [(0, 3), (0, 4), (1, 3), (1, 4)]
        elif number == 3:
            pixels = [(0, 0), (0, 1), (1, 0), (1, 1)]
        elif number == 4:
            pixels = [(3, 6), (3, 7), (4, 6), (4, 7)]
        elif number == 5:
            pixels = [(3, 3), (3, 4), (4, 3), (4, 4)]
        elif number == 6:
            pixels = [(3, 0), (3, 1), (4, 0), (4, 1)]
        elif number == 7:
            pixels = [(6, 6), (6, 7), (7, 6), (7, 7)]
        elif number == 8:
            pixels = [(6, 3), (6, 4), (7, 3), (7, 4)]
        elif number == 9:
            pixels = [(6, 0), (6, 1), (7, 0), (7, 1)]
        else:
            pixels = []

        for pixel in pixels:
            draw.point(pixel, fill="white")

    sleep(2)

try:
    while True:
        clear_display()
        random_number = random.randint(1, 9)
        print(random_number)
        light_pixels_for_number(random_number)

except KeyboardInterrupt:
    pass
finally:
    device.cleanup()

