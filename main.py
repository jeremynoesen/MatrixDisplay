#!/usr/bin/env python

"""
Main file for MatrixDisplay operations. This should be set to run on boot.
"""

import unicornhat as unicorn
from graphics import boot
from server import server

# Initialize the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)

# Show boot animation
boot.show()

# Start server control server
server.start()
