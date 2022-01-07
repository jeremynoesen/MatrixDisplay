"""
Display a solid color on the Unicorn HAT
"""
import time

import unicornhat as unicorn
from graphics import display
from PIL import ImageColor
import threading

current_color = ""
color_thread = None


def __show(hex_color):
    """
    Show a solid color on the Unicorn HAT
    :param hex_color: hex color code
    """
    global current_color
    current_color = hex_color
    color = ImageColor.getcolor(f"#{hex_color}", "RGB")

    thread = threading.currentThread()

    # Fade in
    if getattr(thread, "loop", True):
        fade = threading.Thread(target=display.fade, args=(0, 100, 0.2))
        fade.start()

    # Show color
    while getattr(thread, "loop", True):
        for i in range(8):
            for j in range(8):
                display.set_pixel(i, j, color[0], color[1], color[2])
        unicorn.show()
        time.sleep(1)


def show(hex_color):
    """
    Show a solid color on the Unicorn HAT
    :param hex_color: hex color code
    """
    global color_thread
    color_thread = threading.Thread(target=__show, args=(hex_color,))
    color_thread.start()
