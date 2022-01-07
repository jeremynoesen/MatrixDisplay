"""
Display a solid color on the Unicorn HAT
"""

from graphics import display
from PIL import ImageColor

current_color = ""


def show(hex_color):
    """
    Show a solid color on the Unicorn HAT
    :param hex_color: hex color code
    """
    global current_color
    current_color = hex_color
    color = ImageColor.getcolor(f"#{hex_color}", "RGB")
    for i in range(8):
        for j in range(8):
            display.set_pixel(i, j, color[0], color[1], color[2])
    display.fade(0, 100, 0.2)
