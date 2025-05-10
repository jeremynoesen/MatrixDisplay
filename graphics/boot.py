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
    unicorn.brightness(0.5)
    for i in range(len(display.loading_indicator)):
        for j in range(2):
            x = (j * 127) + 128
            display.set_pixel(display.loading_indicator[i][0], display.loading_indicator[i][1], x, x, x)
            time.sleep(display.frame_delay)
    display.fade(50, 100, 0.05)
    display.fade(100, 0, 1)
    unicorn.clear()
