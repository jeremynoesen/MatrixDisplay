#!/usr/bin/env python3

"""
Main file for MatrixDisplay operations. This should be set to run on boot.
"""

from graphics import boot, display
from server import server

# Start display updates
display.start()

# Show boot animation
boot.show()

# Start control server
server.start()
