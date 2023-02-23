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
fade_thread = None


def __show():
    """
    Show a solid color on the Unicorn HAT
    """
    thread = threading.current_thread()

    # Fade in
    if getattr(thread, "loop", True):
        global fade_thread
        fade_thread = threading.Thread(target=display.fade, args=(0, 100, 0.2))
        fade_thread.start()

    # Show color
    while getattr(thread, "loop", True):
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
