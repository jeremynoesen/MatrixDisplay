"""
A simple web server and interface used to easily control the Unicorn HAT
"""
import time
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

# - >

        # Send the HTML over to create the web page
        time.sleep(0.5)
        with open("./server/index.html") as fd:
            html = fd.read()

            # Process requests
            if self.path.startswith("/image/"):
                display.clear()
                file = self.path.replace("/image/", "")
                image.show(file, True)
                html = html.replace("{imagemode}", ">")
            elif self.path.startswith("/slideshow/"):
                try:
                    display.clear()
                    display_time = int(self.path.replace("/slideshow/", ""))
                    slideshow.set_display_time(display_time)
                    slideshow.show(config.pictures_dir)
                    html = html.replace("{slideshowmode}", ">")
                except ValueError:
                    display.clear()
                    return
            elif self.path.startswith("/color/"):
                display.clear()
                color.current_color = self.path.replace("/color/", "")
                color.show()
                html = html.replace("{colormode}", ">")
            elif self.path == "/off":
                display.clear()
                html = html.replace("{offmode}", ">")
            elif self.path.startswith("/brightness/"):
                try:
                    brightness = int(self.path.replace("/brightness/", ""))
                    display.set_brightness(brightness)
                except ValueError:
                    display.clear()
                    return
            elif self.path.startswith("/warmth/"):
                try:
                    warmth = int(self.path.replace("/warmth/", ""))
                    display.set_warmth(warmth)
                except ValueError:
                    display.clear()
                    return

            # Send the HTML over to create the web page
            time.sleep(0.5)
            html = html.replace("{links_str}", links_str) \
                .replace("{image}", str(image.current_image)) \
                .replace("{duration}", str(slideshow.display_time)) \
                .replace("{color}", color.current_color) \
                .replace("{brightness}", str(display.get_brightness())) \
                .replace("{warmth}", str(display.current_warmth)) \
                .replace("{imagemode}", "-") \
                .replace("{slideshowmode}", "-") \
                .replace("{colormode}", "-") \
               .replace("{offmode}", "-")
            self.do_HEAD()
            self.wfile.write(html.encode("utf-8"))


def start():
    """
    Start the web control panel server
    """
    http_server = HTTPServer(("", 8080), Server)
    http_server.serve_forever()
