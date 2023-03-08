#!/usr/bin/env python3

"""
Main file for MatrixDisplay operations. This should be set to run on boot.
"""

from graphics import display
from server import server
import threading

# Start display updates
threading.Thread(target=display.start).start()

# Start control server
threading.Thread(target=server.start).start()
