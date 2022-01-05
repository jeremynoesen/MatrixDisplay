"""
Show a slideshow of images on the Unicorn HAT
"""

import time
import os
from PIL import Image
from graphics import loading, image, display
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
    files.sort()

    while getattr(thread, "loop", True):
        # Show image
        image.show(Image.open(f"{pictures_dir}/{files[index]}"), False)

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

        # Clear image
        image.clear()


def show(pictures_dir):
    """
    Show the slideshow on the Unicorn HAT
    :param pictures_dir: directory where images are stored
    """
    global slideshow_thread
    slideshow_thread = threading.Thread(target=__show, args=(pictures_dir,))
    slideshow_thread.start()
