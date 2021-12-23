"""
Animations used on the Unicorn HAT
"""

import time
import unicornhat as unicorn


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
