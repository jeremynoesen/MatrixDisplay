"""
Display actions and effects for the Unicorn HAT
"""

import unicornhat as unicorn
import time
from graphics import image, slideshow, loading, color

current_warmth = 0
current_brightness = 1.0


def set_pixel(x, y, r, g, b):
    """
    Set the color of a pixel
    :param x: Matrix pixel x coordinate
    :param y: Matrix pixel y coordinate
    :param r: Red value
    :param g: green value
    :param b: blue value
    """
    unicorn.set_pixel(x, y,
                      int(r * current_brightness),
                      int(max(g - current_warmth, 0) * current_brightness),
                      int(max(b - (current_warmth * 3), 0) * current_brightness))


def set_warmth(warmth):
    """
    Set blue light filter amount
    :param warmth: 0 to 100 intensity of blue light filter
    """
    global current_warmth
    current_warmth = min(max(warmth, 0), 100)


def get_warmth():
    """
    Get the warmth of the display
    :return: Warmth of the display 0 to 100
    """
    return current_warmth


def set_brightness(brightness):
    """
    Set software display brightness
    :param brightness: 0 to 100 brightness of display
    """
    global current_brightness
    current_brightness = min(max(brightness, 0), 100) / 100.0


def get_brightness():
    """
    Get the software display brightness
    :return: Brightness of display 0 to 100
    """
    return int(current_brightness * 100)


def fade(start, end, duration):
    """
    Fade in or out the Unicorn HAT
    :param start: Starting brightness 0 to 100
    :param end: Ending brightness 0 to 100
    :param duration: Duration of fade in seconds
    """
    if end > start:  # Fade in
        sleep_time = duration / float(end - start)
        for i in range(start, end + 1):
            unicorn.brightness(i / 100.0)
            unicorn.show()
            time.sleep(sleep_time)
    elif start > end:  # Fade out
        sleep_time = duration / float(start - end)
        for i in range(end, start + 1):
            unicorn.brightness((start + end - i) / 100.0)
            unicorn.show()
            time.sleep(sleep_time)


def clear():
    """
    Clear the display of the Unicorn HAT
    """
    fade(100, 0, 1)

    loading.clear(False)
    if image.image_thread is not None:
        image.image_thread.loop = False
    if slideshow.slideshow_thread is not None:
        slideshow.slideshow_thread.loop = False

    time.sleep(1)
    unicorn.off()
