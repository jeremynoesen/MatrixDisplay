"""
Show a slideshow of images on the Unicorn HAT
"""

import time
import os
import unicornhat as unicorn
from graphics import loading, image
import threading

slideshow_thread = None
display_time = 30


def __show(pictures_dir):
    """
    Show the slideshow on the Unicorn HAT
    :param pictures_dir: directory where images are stored
    """
    thread = threading.currentThread()
    index = 0
    files = os.listdir(pictures_dir)

    while getattr(thread, "loop", True):
        # Show image
        image.show(files[index], False)

        # Get next index
        if index < len(files) - 1:
            index += 1
        else:
            index = 0

        # Wait for image to load
        time.sleep(3)
        while loading.loading:
            time.sleep(1)

        # Show image for set amount of time
        time.sleep(display_time)


def show(pictures_dir):
    """
    Show the slideshow on the Unicorn HAT
    :param pictures_dir: directory where images are stored
    """
    clear()
    global slideshow_thread
    slideshow_thread = threading.Thread(target=__show, args=(pictures_dir,))
    slideshow_thread.start()


def clear():
    """
    Stop the slideshow
    """
    if slideshow_thread is not None:
        image.clear()
        slideshow_thread.loop = False
        time.sleep(1)
        unicorn.clear()
