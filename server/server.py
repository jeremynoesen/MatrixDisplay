"""
A simple web server and interface used to easily control the Unicorn HAT
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

from graphics import filter, image
import os
from PIL import Image

pictures_dir = "/home/pi/Pictures"


class Server(BaseHTTPRequestHandler):
    """
    Simple web server to control the Unicorn HAT
    """

    def do_HEAD(self):
        """
        Response headers
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        Process requests for displaying for GET requests
        """
        # Get pictures from Pictures folder on Pi
        files = os.listdir(pictures_dir)
        links = []
        files.sort()
        for file in files:
            links.append(f"<a href=\"/image/{file}\">{file}</a>")
        links_str = str(links).removeprefix("[").removesuffix("]").replace("'", "")

        # Send the HTML over to create the web page
        with open("./server/index.html") as fd:
            html = fd.read().replace("{links_str}", links_str) \
                .replace("{brightness}", str(filter.get_brightness())) \
                .replace("{warmth}", str(filter.current_warmth))
            self.do_HEAD()
            self.wfile.write(html.encode("utf-8"))

        # Process requests
        if self.path.startswith("/image/"):
            file = self.path.replace("/image/", "")
            image.show(Image.open(f"{pictures_dir}/{file}"))
        elif self.path.startswith("/brightness/"):
            brightness = int(self.path.replace("/brightness/", ""))
            filter.set_brightness(brightness)
        elif self.path.startswith("/warmth/"):
            warmth = int(self.path.replace("/warmth/", ""))
            filter.set_warmth(warmth)
        elif self.path == "/off":
            image.clear()


def start():
    """
    Start the web control panel server
    """
    http_server = HTTPServer(("", 8080), Server)
    http_server.serve_forever()
