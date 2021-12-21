#!/usr/bin/env python

"""
Main file for PiMatrixDisplay operations. This should be set to run on boot.
"""

import unicornhat as unicorn
import animation
import boot

try:
    # Initialize the Unicorn HAT
    unicorn.set_layout(unicorn.HAT)
    unicorn.rotation(270)

    # Show boot animation
    boot.show_animation()



except KeyboardInterrupt:
    print("Stopping.")
    animation.fade(100, 0, 1)
