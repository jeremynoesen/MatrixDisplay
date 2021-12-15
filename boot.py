#!/usr/bin/env python

"""
Play the boot animation. This would be set up to run automatically on boot.

Usage: sudo python boot.py
"""

import time
import unicornhat as unicorn

# Initialize the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)
unicorn.brightness(0.5)

# Pixels in order of animation
pixels = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
          (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7),
          (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0),
          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]

# Do pixel animation
j = 0
for j in range(len(pixels)):
    pixel = pixels[j]
    j += 1
    unicorn.set_pixel(pixel[0], pixel[1], 255, 255, 255)
    unicorn.show()
    time.sleep(0.07 - (j * 0.002))

# Fade in
i = 0.5
while i < 1.0:
    unicorn.brightness(i)
    unicorn.show()
    i = min(i + 0.05, 1.0)
    time.sleep(0.01)

# Fade out
while i > 0.0:
    unicorn.brightness(i)
    unicorn.show()
    i = max(i - 0.008, 0.0)
    time.sleep(0.01)
