"""
Simple blue light filter for the Unicorn HAT
"""

import unicornhat as unicorn

filter_enabled = False
filter_intensity = 30


def set_pixel(x, y, r, g, b):
    """
    Set the color of a pixel with or without the blue light filter
    :param x: Matrix pixel x coordinate
    :param y: Matrix pixel y coordinate
    :param r: Red value
    :param g: green value
    :param b: blue value
    """
    if filter_enabled is True:
        unicorn.set_pixel(x, y, r, max(g - filter_intensity, 0), max(b - (filter_intensity * 3), 0))
    else:
        unicorn.set_pixel(x, y, r, g, b)


def set_filter_enabled(enabled):
    """
    Enable or disable the blue light filter
    :param enabled: True to enable filter
    """
    global filter_enabled
    filter_enabled = enabled


def set_filter_intensity(intensity):
    """
    Set filter intensity
    :param intensity: 0 to 100 intensity of filter
    """
    global filter_intensity
    filter_intensity = intensity
