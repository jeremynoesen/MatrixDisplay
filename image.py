"""
Draw an image of any size to the Unicorn HAT. Images will be scaled to fit a 1:1 aspect ratio. The scaling algorithm
will divide the image up into an 8 by 8 grid, evenly among the x and y axes. The average color per grid block will be
mapped directly to one LED on the matrix. Essentially, this applies a pixelating filter.
"""

import time
from PIL import Image
import unicornhat as unicorn
from animation import transition
import filter
import threading

thread = None


def __show(input_image):
    """
    Show an image on the Unicorn HAT. Must be run in a separate thread to not lock up!
    """
    # Process all frames of image before displaying
    frame_count = getattr(input_image, "n_frames", 1)
    processed_frames = [[[(0, 0, 0)] * 8 for i in range(8)] for j in range(frame_count)]
    frame_durations = []

    # Get values needed for filtering
    scale_x = int(input_image.size[0] / 8)
    scale_y = int(input_image.size[1] / 8)
    offset_x = int((input_image.size[0] % 8) / 2)
    offset_y = int((input_image.size[1] % 8) / 2)

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
                for block_x in range((matrix_x * scale_x) + offset_x, ((matrix_x * scale_x) + scale_x) + offset_x):
                    for block_y in range((matrix_y * scale_y) + offset_y, ((matrix_y * scale_y) + scale_y) + offset_y):
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
            frame_durations.append(1)

    # Display frames of image on a loop
    current_frame_index = 0
    faded_in = False

    t = threading.currentThread()
    while getattr(t, "loop", True):
        current_frame = processed_frames[current_frame_index]

        # Draw image
        for matrix_x in range(8):
            for matrix_y in range(8):
                pixel = current_frame[matrix_x][matrix_y]
                filter.set_pixel(matrix_x, matrix_y, pixel[0], pixel[1], pixel[2])
        unicorn.show()

        # Fade in if showing for the first time
        if faded_in is False:
            faded_in = True
            transition.fade(0, 100, 0.2)

        # Wait before next frame
        time.sleep(frame_durations[current_frame_index])

        # Increment frame counter
        if current_frame_index < frame_count - 1:
            current_frame_index += 1
        else:
            current_frame_index = 0

    # Fade image out
    transition.fade(100, 0, 1)


def show(image):
    """
    Show an image on the Unicorn HAT
    :param image: Image to show
    """
    global thread
    clear()
    time.sleep(2)
    thread = threading.Thread(target=__show, args=(image,))
    thread.start()


def clear():
    """
    Clear the image off of the Unicorn HAT
    """
    if thread is not None:
        thread.loop = False
