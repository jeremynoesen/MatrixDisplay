#!/usr/bin/env python

"""
Animations used on the Unicorn HAT
"""

import time
import unicornhat as unicorn


def fade_in(start, end, duration):
    sleep_time = duration / float(end - start)
    for i in range(start, end + 1):
        unicorn.brightness(max(i / 100.0, 0.25))
        unicorn.show()
        time.sleep(sleep_time)


def fade_out(start, end, duration):
    sleep_time = duration / float(end - start)
    for i in range(end, start + 1):
        unicorn.brightness(max((100 - i + end) / 100.0, 0.25))
        unicorn.show()
        time.sleep(sleep_time)
