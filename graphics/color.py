"""
Display a solid color on the Unicorn HAT
"""

import time
import unicornhat as unicorn
from graphics import display
from PIL import ImageColor
import threading

current_color = "ffffff"
color_thread = None


def __show():
    """
    Show a solid color on the Unicorn HAT
    """
    thread = threading.currentThread()

    # Fade in
    if getattr(thread, "loop", True):
        fade = threading.Thread(target=display.fade, args=(0, 100, 0.2))
        fade.start()

    # Show color
    while getattr(thread, "loop", True):
        color = ImageColor.getcolor(f"#{current_color}", "RGB")
        for i in range(8):
            for j in range(8):
                display.set_pixel(i, j, color[0], color[1], color[2])
        unicorn.show()
        time.sleep(1)


def show():
    """
    Show a solid color on the Unicorn HAT
    """
    global color_thread
    color_thread = threading.Thread(target=__show)
    color_thread.start()
