"""
A simple web server and interface used to easily control the Unicorn HAT
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

from graphics import display, image, slideshow, color
import os
import config


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
        files = os.listdir(config.pictures_dir)
        links = []
        files.sort()
        for file in files:
            links.append(f"<a href=\"/image/{file}\">{file}</a>")
        links_str = str(links).removeprefix("[").removesuffix("]").replace("'", "")

        # Send the HTML over to create the web page
        with open("./server/index.html") as fd:
            html = fd.read().replace("{links_str}", links_str) \
                .replace("{duration}", str(slideshow.display_time)) \
                .replace("{color}", color.current_color) \
                .replace("{brightness}", str(display.get_brightness())) \
                .replace("{warmth}", str(display.current_warmth))
            self.do_HEAD()
            self.wfile.write(html.encode("utf-8"))

        # Process requests
        if self.path.startswith("/image/"):
            file = self.path.replace("/image/", "")
            display.clear()
            image.show(file, True)
        elif self.path == "/slideshow":
            display.clear()
            slideshow.show(config.pictures_dir)
        elif self.path.startswith("/slideshow/"):
            display_time = int(self.path.replace("/slideshow/", ""))
            slideshow.set_display_time(display_time)
        elif self.path == "/color":
            display.clear()
            color.show()
        elif self.path.startswith("/color/"):
            color.current_color = self.path.replace("/color/", "")
        elif self.path == "/off":
            display.clear()
        elif self.path.startswith("/brightness/"):
            brightness = int(self.path.replace("/brightness/", ""))
            display.set_brightness(brightness)
        elif self.path.startswith("/warmth/"):
            warmth = int(self.path.replace("/warmth/", ""))
            display.set_warmth(warmth)


def start():
    """
    Start the web control panel server
    """
    http_server = HTTPServer(("", 8080), Server)
    http_server.serve_forever()
