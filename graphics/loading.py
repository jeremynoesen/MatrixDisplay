"""
Simple loading animation to show when the device is processing
"""

import time
import unicornhat as unicorn
from graphics import display
import threading

loading_thread = None
loading = False


def __show():
    """
    Show the loading animation. Must be run in a separate thread!
    """
    thread = threading.current_thread()
    pixels = [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6),
              (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    while getattr(thread, "loop", True):
        for i in range(len(pixels)):
            if not getattr(thread, "loop", True):
                break
            for j in range(10):
                pixel = pixels[(i + j + 1) % len(pixels)]
                pixel2 = pixels[(i - j + len(pixels)) % len(pixels)]
                x = 255 - (j * 20)
                display.set_pixel(pixel[0], pixel[1], x, x, x)
                display.set_pixel(pixel2[0], pixel2[1], x, x, x)
            time.sleep(0.0333)


def show(animated: bool):
    """
    Start the loading indicator
    :param animated: True to animate the loading animation
    """
    if animated:
        global loading_thread
        loading_thread = threading.Thread(target=__show)
        loading_thread.start()
        display.fade(0, 100, 0.2)
    global loading
    loading = True


def clear(animated: bool):
    """
    Clear the loading animation off of the Unicorn HAT
    :param animated: True to animate clearing the loading animation
    """
    global loading_thread
    if loading_thread is not None:
        if animated:
            display.fade(100, 0, 0.2)
        loading_thread.loop = False
        loading_thread = None
        unicorn.clear()
    global loading
    loading = False
