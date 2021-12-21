#!/usr/bin/env python

"""
Simple blue light filter for the Unicorn HAT
"""

import unicornhat as unicorn

filter_enabled = False


def set_pixel(x, y, r, g, b):
    if filter_enabled:
        unicorn.set_pixel(x, y, r, max(g - 50, 0), max(b - 100, 0))
    else:
        unicorn.set_pixel(x, y, r, g, b)


def enable_filter(enabled):
    filter.filter_enabled = enabled
