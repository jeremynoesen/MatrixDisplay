"""
Simple loading animation to show when the device is processing
"""

import time
import unicornhat as unicorn
from graphics import display
import threading

loading_thread = None
loading = False
fade_thread = None


def __show():
    """
    Show the loading animation
    """
    thread = threading.current_thread()

    # Pixels in order of animation
    pixels = [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6),
              (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]

    # Fade in
    global fade_thread
    fade_thread = threading.Thread(target=display.fade, args=(0, 100, 0.2))
    fade_thread.start()

    # Do pixel animation
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


def show(animated):
    """
    Show the loading animation on the Unicorn HAT
    :param animated: true to animate the loading animation
    """
    if animated:
        global loading_thread
        loading_thread = threading.Thread(target=__show)
        loading_thread.start()
    global loading
    loading = True


def clear(animated):
    """
    Clear the loading animation off of the Unicorn HAT
    :param animated: true to animate clearing the loading animation
    """
    global loading_thread, fade_thread
    if loading_thread is not None:
        if fade_thread is not None:
            fade_thread.join()
            fade_thread = None
        if animated:
            display.fade(100, 0, 0.2)
        loading_thread.loop = False
        loading_thread.join()
        loading_thread = None
        unicorn.clear()
    global loading
    loading = False
