"""
Simple blue light filter for the Unicorn HAT
"""

import unicornhat as unicorn

current_warmth = 0
current_brightness = 1.0


def set_pixel(x, y, r, g, b):
    """
    Set the color of a pixel with or without the blue light filter
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
    current_warmth = warmth


def set_brightness(brightness):
    """
    Set software display brightness
    :param brightness: 0 to 100 brightness of display
    """
    global current_brightness
    current_brightness = brightness / 100.0
