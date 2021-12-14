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

try:
    # Configure the Unicorn HAT
    unicorn.set_layout(unicorn.HAT)
    unicorn.rotation(270)
    unicorn.brightness(1)

    # Load image
    print(f"Loading image: {str(sys.argv[1])}")
    input_image = Image.open(str(sys.argv[1]))

    # Process all frames of image before displaying
    print("Processing image; this may take a while!")
    frame_count = getattr(input_image, "n_frames", 1)
    processed_frames = [[[(0, 0, 0)] * 8 for i in range(8)] for j in range(frame_count)]
    frame_durations = []

    # Get scale factors for filtering
    scale_x = int(input_image.size[0] / 8)
    scale_y = int(input_image.size[1] / 8)

    # Apply filtering
    for i in range(frame_count):
        input_image.seek(i)

        # Draw black background behind image
        background = Image.new("RGBA", input_image.size, (0, 0, 0))
        image = Image.alpha_composite(background, input_image.convert("RGBA"))

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

                # Store processed pixel
                processed_frames[i][matrix_x][matrix_y] = (r, g, b)

        # Store frame duration
        if getattr(input_image, "is_animated", False) is True:
            frame_durations.append(input_image.info['duration'] / 1000.0)
        else:
            frame_durations.append(60)

    # Display frames of image on a loop
    print("Displaying image.")
    current_frame_index = 0
    while True:
        current_frame = processed_frames[current_frame_index]

        # Draw image
        for matrix_x in range(8):
            for matrix_y in range(8):
                unicorn.set_pixel(matrix_x, matrix_y, current_frame[matrix_x][matrix_y])
        unicorn.show()

        # Wait before next frame
        time.sleep(frame_durations[current_frame_index])

        # Increment frame counter
        if current_frame_index < frame_count - 1:
            current_frame_index += 1
        else:
            current_frame_index = 0

except KeyboardInterrupt:
    print("Stopping.")
