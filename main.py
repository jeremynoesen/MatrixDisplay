#!/usr/bin/env python

"""
Main file for MatrixDisplay operations. This should be set to run on boot.
"""

import unicornhat as unicorn
from animation import boot
from http.server import HTTPServer
from server import requests

# Initialize the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)

# Show boot animation
boot.show_animation()

# Start server control server
http_server = HTTPServer(("matrixdisplay.local", 8080), requests.Server)
http_server.serve_forever()
