"""
Simple loading animation to show when the device is processing
"""

import time
import unicornhat as unicorn
from animation import transition
import filter
import threading

loadingthread = None


def __show():
    """
    Show the loading animation
    """
    unicorn.brightness(1)

    # Pixels in order of animation
    pixels = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
              (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7),
              (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0),
              (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]

    faded_in = False
    t = threading.currentThread()
    while getattr(t, "loop", True):

        # Do pixel animation
        for i in range(len(pixels)):
            unicorn.clear()

            if not getattr(t, "loop", True):
                break

            for j in range(8):
                pixel = pixels[(i + j) % len(pixels)]
                filter.set_pixel(pixel[0], pixel[1], 255, 255, 255)

                # Initial fade in
                if faded_in is False:
                    time.sleep(0.03)
                    unicorn.show()
            unicorn.show()

            faded_in = True

            # Wait before next frane
            time.sleep(0.03)


def show():
    """
    Show the loading animation on the Unicorn HAT
    """
    clear()
    global loadingthread
    loadingthread = threading.Thread(target=__show)
    loadingthread.start()


def clear():
    """
    Clear the loading animation off of the Unicorn HAT
    """
    if loadingthread is not None:
        transition.fade(100, 0, 0.2)
        loadingthread.loop = False
        time.sleep(0.03)
        unicorn.clear()