#!/usr/bin/env python3

"""
Main file for MatrixDisplay. This should be set to run on boot.
"""

from graphics import boot, display
from server import server

if __name__ == "__main__":
    display.start()
    boot.show()
    server.start()
