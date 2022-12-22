"""
Show a slideshow of images on the Unicorn HAT
"""

import time
import os
from graphics import loading, image
import threading

slideshow_thread = None
display_time = 30


def __show(pictures_dir):
    """
    Show the slideshow on the Unicorn HAT
    :param pictures_dir: directory where images are stored
    """
    thread = threading.current_thread()
    index = 0
    files = os.listdir(pictures_dir)
    files.sort()

    while getattr(thread, "loop", True):
        # Show image
        image.show(files[index], False)

        # Get next index
        if index < len(files) - 1:
            index += 1
        else:
            index = 0

        # Wait for image to load
        time.sleep(0.2)
        while loading.loading:
            time.sleep(0.2)

        # Show image for set amount of time
        time.sleep(display_time)

        # Clear image
        if getattr(thread, "loop", True):
            image.clear()


def show(pictures_dir):
    """
    Show the slideshow on the Unicorn HAT
    :param pictures_dir: directory where images are stored
    """
    global slideshow_thread
    slideshow_thread = threading.Thread(target=__show, args=(pictures_dir,))
    slideshow_thread.start()


def set_display_time(time):
    """
    Set the display time for images in the slideshow
    :param time: time in seconds to display images
    """
    global display_time
    display_time = max(1, time)
