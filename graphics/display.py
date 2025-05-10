"""
Display actions and effects for the Unicorn HAT
"""

import threading
import unicornhat as unicorn
import time
from graphics import image, slideshow, loading, color

unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)
current_warmth = 0
current_brightness = 100
modified_brightness = 1.0
frame_delay = 1 / 30
loading_indicator = [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6),
          (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]


def set_pixel(x: int, y: int, r: int, g: int, b: int):
    """
    Set the color of a pixel
    :param x: Matrix pixel x coordinate
    :param y: Matrix pixel y coordinate
    :param r: Red value
    :param g: Green value
    :param b: Blue value
    """
    unicorn.set_pixel(x, y,
                      round(r * modified_brightness),
                      round(max(g - (current_warmth * 0.5), 0) * modified_brightness),
                      round(max(b - (current_warmth * 1.5), 0) * modified_brightness))


def set_warmth(warmth: int):
    """
    Set blue light filter intensity
    :param warmth: 0 to 100 intensity of blue light filter
    """
    global current_warmth
    current_warmth = min(max(warmth, 0), 100)


def set_brightness(brightness: int):
    """
    Set software display brightness
    :param brightness: 0 to 100 brightness of display
    """
    global current_brightness, modified_brightness
    current_brightness = min(max(brightness, 0), 100)
    modified_brightness = (((current_brightness * (100 - 17)) / 100) + 17) / 100


def fade(start: int, end: int, duration: float):
    """
    Fade in or out the Unicorn HAT
    :param start: Starting brightness 0 to 100
    :param end: Ending brightness 0 to 100
    :param duration: Duration of fade in seconds
    """
    start_visible = ((start * (100 - 17)) / 100) + 17
    end_visible = ((end * (100 - 17)) / 100) + 17
    delta = 0
    current = 0
    while True:
        start_time = time.time()
        current += delta
        if end > start_visible:
            unicorn.brightness(
                (((min(current, duration) * (end_visible - start_visible)) / duration) + start_visible) / 100)
        else:
            unicorn.brightness(((((duration - min(current, duration)) * (
                    start_visible - end_visible)) / duration) + end_visible) / 100)
        time.sleep(frame_delay)
        if current >= duration:
            break
        delta = time.time() - start_time


def clear():
    """
    Clear the display of the Unicorn HAT
    """
    if image.fade_thread is not None:
        image.fade_thread.join()
        image.fade_thread = None
    fade(100, 0, 0.5)
    if loading.loading_thread is not None:
        loading.loading_thread.loop = False
        loading.loading_thread = None
    if image.image_thread is not None:
        image.image_thread.loop = False
        image.image_thread = None
        image.current_image = ""
    if slideshow.slideshow_thread is not None:
        slideshow.slideshow_thread.loop = False
        slideshow.slideshow_thread = None
        slideshow.display_time = 0
    if color.color_thread is not None:
        color.color_thread.loop = False
        color.color_thread = None
        color.current_color = "000000"
    unicorn.clear()


def __start():
    """
    Update the display of the Unicorn HAT. Must be run in a separate thread!
    """
    while True:
        unicorn.show()
        time.sleep(frame_delay)


def start():
    """
    Start the display update thread
    """
    display_thread = threading.Thread(target=__start)
    display_thread.start()
