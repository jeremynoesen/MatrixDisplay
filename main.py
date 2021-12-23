#!/usr/bin/env python

"""
Main file for PiMatrixDisplay operations. This should be set to run on boot.
"""

import unicornhat as unicorn
import boot
from http.server import HTTPServer
from web import Server

# Initialize the Unicorn HAT
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(270)

# Show boot animation
boot.show_animation()

# Start web control server
http_server = HTTPServer(("matrixdisplay.local", 8080), Server)
http_server.serve_forever()
