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
    Show the slideshow on the Unicorn HAT. Must be run in a separate thread!
    """
    thread = threading.current_thread()
    index = 0
    files = os.listdir(config.pictures_dir)
    random.shuffle(files)
    while getattr(thread, "loop", True):
        if os.path.isfile(f'{config.pictures_dir}{files[index]}') and \
                not files[index].startswith("."):
            image.show(files[index], False)
            if getattr(thread, "loop", True):
                time.sleep(0.5)
                while loading.loading and getattr(thread, "loop", True):
                    time.sleep(0.5)
            if getattr(thread, "loop", True):
                time.sleep(display_time)
            if getattr(thread, "loop", True):
                image.clear()
        else:
            print(f'File {config.pictures_dir}{files[index]} '
                  f'is either a directory, hidden, or doesn\'t exist; skipping it.')
        if index < len(files) - 1:
            index += 1
        else:
            index = 0


def show(time: int):
    """
    Show the slideshow on the Unicorn HAT
    :param time: How long to display images in seconds
    """
    global display_time, slideshow_thread
    display_time = max(1, time)
    slideshow_thread = threading.Thread(target=__show)
    slideshow_thread.start()
