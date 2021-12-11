#!/usr/bin/env python

"""
Draw an image of any size to the Unicorn HAT. Images will be scaled to fit a 1:1 aspect ratio. The scaling algorithm
will divide the image up into an 8 by 8 grid, evenly among the x and y axes. The average color per grid block will be
mapped directly to one LED on the matrix. Essentially, this applies a pixelating filter.

Usage: sudo python show_image.py path/to/image
"""

import sys
import time
from PIL import Image
import unicornhat as unicorn

# Configure the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)
unicorn.brightness(1)

# Load raw image
raw = Image.open(str(sys.argv[1]))

# Get scale factors for filtering
width = raw.size[0]
height = raw.size[1]
scale_x = int(width / 8)
scale_y = int(height / 8)

# Get animation data
frames = getattr(raw, "n_frames", 1)
if getattr(raw, "is_animated", False) is True:
    frame_step = raw.info['duration'] / float(frames)
else:
    frame_step = 60

# Process all frames of image before displaying
processed_frames = [[[(0, 0, 0)] * width for i in range(height)] for j in range(frames)]

for i in range(frames):
    raw.seek(i)

    # Draw black background behind image
    frame = raw.convert("RGBA")
    background = Image.new("RGBA", raw.size, (0, 0, 0))
    image = Image.alpha_composite(background, frame)

    for matrix_x in range(8):
        for matrix_y in range(8):
            r = 0
            g = 0
            b = 0

            # Sum all RGB values in a block of pixels
            for block_x in range(matrix_x * scale_x, (matrix_x * scale_x) + scale_x):
                for block_y in range(matrix_y * scale_y, (matrix_y * scale_y) + scale_y):
                    pixel = image.getpixel((block_x, block_y))
                    r += int(pixel[0])
                    g += int(pixel[1])
                    b += int(pixel[2])

            # Get average RGB values for block
            r = int(r / (scale_x * scale_y))
            g = int(g / (scale_x * scale_y))
            b = int(b / (scale_x * scale_y))

            # Store processed image
            processed_frames[i][matrix_x][matrix_y] = (r, g, b)

# Display frames of image on a loop
current_frame_index = 0
while True:

    # Draw image
    for matrix_x in range(width):
        for matrix_y in range(height):
            unicorn.set_pixel(matrix_x, matrix_y, processed_frames[current_frame_index][matrix_x][matrix_y])
    unicorn.show()

    # Increment frame counter
    if current_frame_index < frames - 1:
        current_frame_index += 1
    else:
        current_frame_index = 0

    # Wait before next frame
    time.sleep(frame_step)
