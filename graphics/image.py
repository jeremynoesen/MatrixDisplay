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
import config
import os

image_thread = None
fade_thread = None


def __save(image_array, file_name):
    """
    Save a processed image to the cache directory
    :param image_array: tuple of processed frames and frame durations
    :param file_name: name of original file
    """
    processed_frames = image_array[0]
    frame_durations = image_array[1]
    frame_count = len(frame_durations)

    # Create cache dir if it does not exist
    if not os.path.exists(config.cache_dir):
        os.mkdir(config.cache_dir)

    # Load processed frames as images
    output_frames = []
    for current_frame in processed_frames:
        output_image = Image.new(mode="RGB", size=(8, 8))

        for x in range(8):
            for y in range(8):
                output_image.putpixel((x, y), current_frame[x][y])
        output_frames.append(output_image)

    # Get file format
    file_name_parts = file_name.split(".")
    image_format = file_name_parts[len(file_name_parts) - 1].upper()

    # Save image file
    output_file = f"{config.cache_dir}{file_name}"
    if frame_count > 1:

        # Get corrected frame durations
        output_durations = [frame_durations[0]]
        for i in range(1, len(frame_durations)):
            output_durations.append(int((frame_durations[i] - frame_durations[i - 1]) * 1000))

        output_frames[0].save(output_file, format=image_format,
                              append_images=output_frames[1:], save_all=True, loop=0, duration=output_durations)
    else:
        output_frames[0].save(output_file, format=image_format)


def __load(image_path, cached):
    """
    Load an image into an array for displaying.
    :param image_path: full path to image to load
    :param cached: True to indicate that a cached image is being loaded. This will skip some parts of the processing.
    """
    thread = threading.currentThread()

    # Load image from disk
    input_image = Image.open(image_path)
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
        if not getattr(thread, "loop", True):
            break
        input_image.seek(i)

        if not cached:
            # Draw black background behind image
            background = Image.new("RGBA", input_image.size, (0, 0, 0))
            image = Image.alpha_composite(background, input_image.convert("RGBA"))
        else:
            image = input_image

        for matrix_x in range(8):
            for matrix_y in range(8):
                if not getattr(thread, "loop", True):
                    break
                r = 0
                g = 0
                b = 0

                # Sum all RGB values in a block of pixels
                for block_x in range((matrix_x * scale_x) + offset_x, ((matrix_x * scale_x) + scale_x) + offset_x):
                    for block_y in range((matrix_y * scale_y) + offset_y, ((matrix_y * scale_y) + scale_y) + offset_y):
                        if not getattr(thread, "loop", True):
                            break
                        pixel = image.getpixel((block_x, block_y))
                        r += int(pixel[0])
                        g += int(pixel[1])
                        b += int(pixel[2])

                if not cached:
                    # Get average RGB values for block
                    r = int(r / (scale_x * scale_y))
                    g = int(g / (scale_x * scale_y))
                    b = int(b / (scale_x * scale_y))

                # Store processed pixel
                processed_frames[i][matrix_x][matrix_y] = (r, g, b)

        # Store frame duration
        if frame_count > 1:
            duration = input_image.info['duration'] / 1000.0
            duration_sum += duration
            frame_durations.append(duration_sum)

    # Return image array and durations
    return processed_frames, frame_durations


def __draw(image_array):
    """
    draw the image on the Unicorn HAT
    :param image_array: tuple of the processed frames and the frame durations
    """
    thread = threading.currentThread()
    processed_frames = image_array[0]
    frame_durations = image_array[1]
    frame_count = len(frame_durations)

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
        if frame_count > 1:
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


def __show(file_name):
    """
    Show an image on the Unicorn HAT. Must be run in a separate thread to not lock up!
    :param file_name: Name of image file to show
    """
    thread = threading.currentThread()

    if os.path.exists(f"{config.cache_dir}{file_name}"):
        # Get cached image
        display_image = __load(f"{config.cache_dir}{file_name}", True)
    else:
        # Start loading indicator
        if getattr(thread, "loop", True):
            loading.show()

        # Get and process image
        display_image = __load(f"{config.pictures_dir}{file_name}", False)

        # Save image to cached folder
        if getattr(thread, "loop", True):
            __save(display_image, file_name)

        # Clear loading indicator
        if getattr(thread, "loop", True):
            loading.clear(True)

    # Fade in image
    if getattr(thread, "loop", True):
        global fade_thread
        fade_thread = threading.Thread(target=display.fade, args=(0, 100, 0.2))
        fade_thread.start()

    # Draw image to display
    __draw(display_image)


def show(file_name):
    """
    Show an image on the Unicorn HAT
    :param file_name: Name of image to show
    """
    global image_thread
    image_thread = threading.Thread(target=__show, args=(file_name,))
    image_thread.start()


def clear():
    """
    Clear the image off of the Unicorn HAT
    """
    if image_thread is not None:
        if fade_thread is not None:
            fade_thread.join()
        display.fade(100, 0, 0.5)
        loading.clear(False)
        image_thread.loop = False
        image_thread.join()
        unicorn.clear()
