"""
Simple boot animation used to show when the board is ready to use.
"""

import time
import unicornhat as unicorn
from graphics import transition, filter


def show():
    """
    Show the boot animation
    """
    unicorn.brightness(0.5)

    # Pixels in order of animation
    pixels = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
              (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7),
              (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0),
              (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]

    # Do pixel animation
    for i in range(len(pixels)):
        pixel = pixels[i]
        filter.set_pixel(pixel[0], pixel[1], 255, 255, 255)
        unicorn.show()
        time.sleep(0.06 - (i * 0.0015))

    # Fade in then out
    transition.fade(50, 100, 0.1)
    transition.fade(100, 0, 1)

    # Clear screen
    unicorn.clear()
