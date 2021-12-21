"""
Simple blue light filter for the Unicorn HAT
"""

import unicornhat as unicorn

filter_enabled = False


def set_pixel(x, y, r, g, b):
    """
    Set the color of a pixel with or without the blue light filter
    :param x: Matrix pixel x coordinate
    :param y: Matrix pixel y coordinate
    :param r: Red value
    :param g: green value
    :param b: blue value
    """
    if filter_enabled:
        unicorn.set_pixel(x, y, r, max(g - 50, 0), max(b - 100, 0))
    else:
        unicorn.set_pixel(x, y, r, g, b)


def enable_filter(enabled):
    """
    Enable or disable the blue light filter
    :param enabled: True to enable filter
    """
    filter.filter_enabled = enabled
