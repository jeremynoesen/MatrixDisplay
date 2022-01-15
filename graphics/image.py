"""
Draw an image of any size to the Unicorn HAT. Images will be scaled to fit a 1:1 aspect ratio. The scaling algorithm
will divide the image up into an 8 by 8 grid, evenly among the x and y axes. The average color per grid block will be
mapped directly to one LED on the matrix. Essentially, this applies a pixelating filter.
"""

import time
from PIL import Image
import unicornhat as unicorn
from graphics import loading, display
import threading

image_thread = None


def __show(input_image, show_loading):
    """
    Show an image on the Unicorn HAT. Must be run in a separate thread to not lock up!
    :param input_image: Image to show
    :param show_loading: True to show loading animation
    """
    thread = threading.currentThread()

    # Show loading animation
    if getattr(thread, "loop", True):
        loading.show(show_loading)

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
    duration_sum = 0
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
            duration = input_image.info['duration'] / 1000.0
            duration_sum += duration
            frame_durations.append(duration_sum)

    # Clear loading animation and begin fade in
    if getattr(thread, "loop", True):
        loading.clear(show_loading)
        fade = threading.Thread(target=display.fade, args=(0, 100, 0.2))
        fade.start()

    # Display frames of image on a loop
    current_frame_index = 0
    timestamp = 0
    while getattr(thread, "loop", True):
        start_time = time.time()
        current_frame = processed_frames[current_frame_index]

        # Draw image
        for matrix_x in range(8):
            for matrix_y in range(8):
                pixel = current_frame[matrix_x][matrix_y]
                display.set_pixel(matrix_x, matrix_y, pixel[0], pixel[1], pixel[2])

        # Wait before next frame
        time.sleep(0.0167)

        # Increment frame counter
        if getattr(input_image, "is_animated", False) is True:
            timestamp = (timestamp + (time.time() - start_time))  # Use delta time to prevent visual slowdown
            for i in range(frame_count - 1):
                temp_index = current_frame_index + i
                if temp_index < frame_count - 1:
                    if timestamp <= frame_durations[temp_index]:
                        current_frame_index = temp_index
                        break
                else:
                    if timestamp % frame_durations[frame_count - 1] <= frame_durations[temp_index % (frame_count - 1)]:
                        current_frame_index = temp_index % (frame_count - 1)
                        timestamp = timestamp % frame_durations[frame_count - 1]
                        break


def show(image, show_loading):
    """
    Show an image on the Unicorn HAT
    :param image: Image to show
    :param show_loading: True to show loading animation
    """
    global image_thread
    image_thread = threading.Thread(target=__show, args=(image, show_loading))
    image_thread.start()


def clear():
    """
    Clear the image off of the Unicorn HAT
    """
    if image_thread is not None:
        time.sleep(0.2)
        display.fade(100, 0, 0.5)
        loading.clear(False)
        image_thread.loop = False
        time.sleep(0.0167)
        unicorn.clear()
