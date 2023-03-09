"""
Show a slideshow of images on the Unicorn HAT
"""

import time
import os

import config
from graphics import loading, image
import threading
import random

slideshow_thread = None
display_time = 0


def __show():
    """
    Show the slideshow on the Unicorn HAT
    """

    thread = threading.current_thread()
    index = 0
    files = os.listdir(config.pictures_dir)
    random.shuffle(files)

    while getattr(thread, "loop", True):
        # Show image
        image.show(files[index], False)

        # Get next index
        if index < len(files) - 1:
            index += 1
        else:
            index = 0

        # Wait for image to load
        if getattr(thread, "loop", True):
            time.sleep(0.5)
            while loading.loading and getattr(thread, "loop", True):
                time.sleep(0.5)

        # Show image for set amount of time
        if getattr(thread, "loop", True):
            time.sleep(display_time)

        # Clear image
        if getattr(thread, "loop", True):
            image.clear()


def show(time: int):
    """
    Show the slideshow on the Unicorn HAT
    :param time: how long to display images in seconds
    """

    # Parse time
    global display_time
    display_time = max(1, time)

    # Start thread
    global slideshow_thread
    slideshow_thread = threading.Thread(target=__show)
    slideshow_thread.start()
