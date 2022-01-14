#!/usr/bin/env python3

"""
Main file for MatrixDisplay operations. This should be set to run on boot.
"""

import unicornhat as unicorn
from graphics import boot, display
from server import server
import threading

# Initialize the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)

# Start display updates
threading.Thread(target=display.start).start()

# Show boot animation
boot.show()

# Start control server
server.start()
