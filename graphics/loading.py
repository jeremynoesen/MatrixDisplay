"""
Simple loading animation to show when the device is processing
"""

import time
import unicornhat as unicorn
from graphics import transition, filter
import threading

loading_thread = None


def __show():
    """
    Show the loading animation
    """
    thread = threading.currentThread()

    if getattr(thread, "loop", True):
        unicorn.brightness(1)

    # Pixels in order of animation
    pixels = [(4, 0), (5, 0), (6, 1), (7, 2), (7, 3), (7, 4), (7, 5), (6, 6), (5, 7), (4, 7),
              (3, 7), (2, 7), (1, 6), (0, 5), (0, 4), (0, 3), (0, 2), (1, 1), (2, 0), (3, 0)]

    faded_in = False
    while getattr(thread, "loop", True):

        # Do pixel animation
        for i in range(len(pixels)):

            if not getattr(thread, "loop", True):
                break
            else:
                unicorn.clear()

            for j in range(8):
                pixel = pixels[(i + j) % len(pixels)]
                filter.set_pixel(pixel[0], pixel[1], 45 + (j * 30), 45 + (j * 30), 45 + (j * 30))

                # Initial fade in
                if faded_in is False:
                    time.sleep(0.04)
                    unicorn.show()
            unicorn.show()

            faded_in = True

            # Wait before next frane
            time.sleep(0.04)


def show():
    """
    Show the loading animation on the Unicorn HAT
    """
    clear()
    global loading_thread
    loading_thread = threading.Thread(target=__show)
    loading_thread.start()


def clear():
    """
    Clear the loading animation off of the Unicorn HAT
    """
    if loading_thread is not None:
        transition.fade(100, 0, 0.2)
        loading_thread.loop = False
        time.sleep(0.04)
        unicorn.clear()


def cancel():
    """
    Clear the loading animation off of the Unicorn HAT without animating
    """
    if loading_thread is not None:
        loading_thread.loop = False
        time.sleep(0.04)
        unicorn.clear()
