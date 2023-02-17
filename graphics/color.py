"""
Display a solid color on the Unicorn HAT
"""

import time
from graphics import display
from PIL import ImageColor
import threading

current_color = "ffffff"
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
        try:
            color = ImageColor.getcolor(f"#{current_color}", "RGB")
            for i in range(8):
                for j in range(8):
                    display.set_pixel(i, j, color[0], color[1], color[2])
            time.sleep(0.0333)
        except ValueError:
            display.clear()
            return


def show():
    """
    Show a solid color on the Unicorn HAT
    """
    global color_thread
    color_thread = threading.Thread(target=__show)
    color_thread.start()
