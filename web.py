from http.server import BaseHTTPRequestHandler

import filter
import image
import os
from PIL import Image


class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        files = os.listdir("/home/pi/Pictures")
        links = []
        for file in files:
            links.append(f"<a href=\"/image/{file}\">{file}</a>")

        html = open("index.html")
        self.do_HEAD()
        if self.path.startswith("/image/"):
            file = self.path.replace("/image/", "")
            image.show_image(Image.open(f"/home/pi/Pictures/{file}"))
        elif self.path.startswith("/brightness/"):
            brightness = int(self.path.replace("/brightness/", ""))
            filter.set_brightness(brightness)
        elif self.path.startswith("/warmth/"):
            warmth = int(self.path.replace("/warmth/", ""))
            filter.set_warmth(warmth)
        elif self.path == "/off":
            image.clear_image()
        self.wfile.write(html.encode("utf-8"))
