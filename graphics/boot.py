"""
Simple boot animation used to show when the board is ready to use.
"""

import time
import unicornhat as unicorn
from graphics import display


def show():
    """
    Show the boot animation
    """
    pixels = [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6),
              (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    unicorn.brightness(0.5)
    for i in range(len(pixels)):
        pixel = pixels[i]
        for j in range(2):
            x = (j * 127) + 128
            display.set_pixel(pixel[0], pixel[1], x, x, x)
            time.sleep(0.0333)
    display.fade(50, 100, 0.05)
    display.fade(100, 0, 1)
    unicorn.clear()
