#!/usr/bin/env python

"""
Draw an image of any size to the Unicorn HAT. Images will be scaled to fit a 1:1 aspect ratio. The scaling algorithm
will divide the image up into an 8 by 8 grid, evenly among the x and y axes. The average color per grid block will be
mapped directly to one LED on the matrix. To use, run the file with one argument, which will be the path to the image.
"""

import sys
from PIL import Image
import unicornhat as unicorn

# Configure the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(90)
unicorn.brightness(0.5)

# Get image and dimensions
image = Image.open(str(sys.argv)[0])
scale_x = int(image.size[0] / 8)
scale_y = int(image.size[1] / 8)

# Draw all pixels of matrix
for matrix_x in range(int(8)):
    for matrix_y in range(int(8)):

        # Reset RGB values for next calculation cycle
        r = 0
        g = 0
        b = 0

        # Sum all RGB values in a block of pixels
        for block_x in range(int(matrix_x * scale_x), int((matrix_x * scale_x) + scale_x - 1)):
            for block_y in range(int(matrix_y * scale_y), int((matrix_y * scale_y) + scale_y - 1)):
                pixel = image.getpixel((block_x, block_y))
                r += int(pixel[0])
                g += int(pixel[1])
                b += int(pixel[2])

        # Get average RGB values for block
        r = int(r / (scale_x * scale_y))
        g = int(g / (scale_x * scale_y))
        b = int(b / (scale_x * scale_y))

        # Show pixel on matrix
        unicorn.set_pixel(matrix_x, matrix_y, r, g, b)
        unicorn.show()
