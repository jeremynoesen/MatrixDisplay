"""
Display actions and effects for the Unicorn HAT
"""

import unicornhat as unicorn
import time
from graphics import image, slideshow, loading, color

current_warmth = 0
current_brightness = 1.0
modified_brightness = 1.0


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
                      int(r * modified_brightness),
                      int(max(g - (current_warmth * 0.5), 0) * modified_brightness),
                      int(max(b - (current_warmth * 1.5), 0) * modified_brightness))


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
    global current_brightness, modified_brightness
    current_brightness = min(max(brightness, 0), 100) / 100.0
    modified_brightness = ((current_brightness * (1.0 - 0.17)) / 1.0) + 0.17


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
    # Map start and end value to visible range
    start_visible = int(((start * (100 - 17)) / 100) + 17)
    end_visible = int(((end * (100 - 17)) / 100) + 17)

    # Do fading with delta time to ensure the fades last exactly the specified duration
    delta = 0
    current = 0
    while True:
        start_time = time.time()
        current += delta
        if end > start_visible:
            unicorn.brightness(
                int(((min(current, duration) * (end_visible - start_visible)) / duration) + start_visible) / 100.0)
        else:
            unicorn.brightness(int((((duration - min(current, duration)) * (
                        start_visible - end_visible)) / duration) + end_visible) / 100.0)
        time.sleep(0.0333)
        delta = time.time() - start_time
        if current >= duration:
            break


def clear():
    """
    Clear the display of the Unicorn HAT
    """
    if loading.fade_thread is not None:
        loading.fade_thread.join()
    if image.fade_thread is not None:
        image.fade_thread.join()
    if color.fade_thread is not None:
        color.fade_thread.join()

    fade(100, 0, 0.5)

    if loading.loading_thread is not None:
        loading.loading_thread.loop = False
        loading.loading_thread.join()
    if image.image_thread is not None:
        image.image_thread.loop = False
        image.image_thread.join()
    if slideshow.slideshow_thread is not None:
        slideshow.slideshow_thread.loop = False
    if color.color_thread is not None:
        color.color_thread.loop = False
        color.color_thread.join()

    unicorn.clear()


def start():
    """
    Update the display of the Unicorn HAT
    """
    while True:
        unicorn.show()
        time.sleep(0.0333)
