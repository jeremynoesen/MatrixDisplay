#!/usr/bin/env python

import sys
from PIL import Image
import unicornhat as unicorn

# Configure the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(90)
unicorn.brightness(0.5)

# Get image and dimensions
img = Image.open(str(sys.argv)[0])
scaleX = int(img.size[0]/8)
scaleY = int(img.size[1]/8)

# Draw all pixels of matrix
for matrixX in range(int(8)):
    for matrixY in range(int(8)):

        r, g, b = 0, 0, 0

        # Sum all colors in a block of pixels
        for blockX in range(int(matrixX * scaleX), int((matrixX * scaleX) + scaleX - 1)):
            for blockY in range(int(matrixY * scaleY), int((matrixY * scaleY) + scaleY - 1)):

                pixel = img.getpixel((blockX, blockY))
                r += int(pixel[0])
                g += int(pixel[1])
                b += int(pixel[2])

        # Average out the color of the block
        r = int(r / (scaleX * scaleY))
        g = int(g / (scaleX * scaleY))
        b = int(b / (scaleX * scaleY))

        # Show pixel data on matrix
        unicorn.set_pixel(matrixX, matrixY, r, g, b)
        unicorn.show()
