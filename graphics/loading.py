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
    while getattr(thread, "loop", True):
        for i in range(len(display.loading_indicator)):
            if not getattr(thread, "loop", True):
                break
            for j in range(10):
                if not getattr(thread, "loop", True):
                    break
                pixel = display.loading_indicator[(i + j + 1) % len(display.loading_indicator)]
                pixel2 = display.loading_indicator[(i - j + len(display.loading_indicator)) % len(display.loading_indicator)]
                x = 255 - (j * 20)
                display.set_pixel(pixel[0], pixel[1], x, x, x)
                display.set_pixel(pixel2[0], pixel2[1], x, x, x)
            if getattr(thread, "loop", True):
                time.sleep(display.frame_delay)


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
