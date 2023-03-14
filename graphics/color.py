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
    Show a solid color on the Unicorn HAT. Must be run in a separate thread!
    """
    thread = threading.current_thread()
    while getattr(thread, "loop", True):
        for i in range(8):
            for j in range(8):
                display.set_pixel(i, j, rgb_color[0], rgb_color[1], rgb_color[2])
        time.sleep(0.0333)


def show(color: str):
    """
    Show a solid color on the Unicorn HAT
    :param color: Hex color to display
    """
    global current_color, rgb_color, color_thread
    rgb_color = ImageColor.getcolor(f"#{color}", "RGB")
    current_color = color
    color_thread = threading.Thread(target=__show)
    color_thread.start()
    display.fade(0, 100, 0.2)
