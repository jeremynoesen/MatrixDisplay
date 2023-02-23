"""
Display a solid color on the Unicorn HAT
"""

import time
from graphics import display
from PIL import ImageColor
import threading

current_color = "000000"
rgb_color = None
color_thread = None


def __show():
    """
    Show a solid color on the Unicorn HAT
    """

    # Fade in
    display.fade_async(0, 100, 0.2)

    # Show color
    while getattr(threading.current_thread(), "loop", True):
        for i in range(8):
            for j in range(8):
                display.set_pixel(i, j, rgb_color[0], rgb_color[1], rgb_color[2])
        time.sleep(0.0333)


def show(color):
    """
    Show a solid color on the Unicorn HAT
    :param color: hex color code to display
    """

    # Parse color
    global current_color, rgb_color
    rgb_color = ImageColor.getcolor(f"#{color}", "RGB")
    current_color = color

    # Start thread
    global color_thread
    color_thread = threading.Thread(target=__show)
    color_thread.start()
