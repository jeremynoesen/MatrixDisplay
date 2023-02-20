"""
A simple web server and interface used to easily control the Unicorn HAT
"""
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from graphics import display, image, slideshow, color
import os
import config

current_mode = "off"


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
        Process GET requests, which includes sending the web panel
        """

        self.do_HEAD()

        global current_mode

        # Get pictures from Pictures folder on Pi and generate buttons
        files = os.listdir(config.pictures_dir)
        links = []
        files.sort()
        for file in files:
            links.append(f'<h4><a href="javascript:image{files.index(file)}()">{file}</a></h4>'
                         f'<script>'
                         f'    function image{files.index(file)}() {{'
                         f'        fetch("/image/{file}", {{method: "post"}})'
                         f'        document.getElementById("imagetitle").textContent = "> Image: {file}"'
                         f'        document.getElementById("slideshowtitle").textContent = "- Slideshow: 0 seconds per image"'
                         f'        document.getElementById("colortitle").textContent = "- Color: #000000"'
                         f'        document.getElementById("offtitle").textContent = "- Off"'
                         f'    }}'
                         f'</script>')
        links_str = str(links).removeprefix("[").removesuffix("]").replace("'", "")

        # Send the HTML over to create the web page
        with open("./server/index.html") as fd:
            html = fd.read().replace("{links_str}", links_str) \
                .replace("{image}", str(image.current_image)) \
                .replace("{duration}", str(slideshow.display_time)) \
                .replace("{color}", color.current_color) \
                .replace("{brightness}", str(display.get_brightness())) \
                .replace("{warmth}", str(display.current_warmth)) \

            if current_mode == "image":
                html = html.replace("{imagemode}", ">")
            elif current_mode == "slideshow":
                html = html.replace("{slideshowmode}", ">")
            elif current_mode == "color":
                html = html.replace("{colormode}", ">")
            elif current_mode == "off":
                html = html.replace("{offmode}", ">")

            html = html.replace("{imagemode}", "-") \
                .replace("{slideshowmode}", "-") \
                .replace("{colormode}", "-") \
                .replace("{offmode}", "-")
            self.wfile.write(html.encode("utf-8"))


    def do_POST(self):
        """
        Process POST requests, which only updates the display
        """

        self.do_HEAD()

        global current_mode

        if self.path.startswith("/image/"):
            display.clear()
            file = self.path.replace("/image/", "")
            image.show(file, True)
            current_mode = "image"
        elif self.path.startswith("/slideshow/"):
            try:
                display.clear()
                display_time = int(self.path.replace("/slideshow/", ""))
                slideshow.set_display_time(display_time)
                slideshow.show(config.pictures_dir)
                current_mode = "slideshow"
            except ValueError:
                display.clear()
                return
        elif self.path.startswith("/color/"):
            display.clear()
            color.current_color = self.path.replace("/color/", "")
            color.show()
            current_mode = "color"
        elif self.path == "/off":
            display.clear()
            current_mode = "off"
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

def start():
    """
    Start the web control panel server
    """
    http_server = HTTPServer(("", 8080), Server)
    http_server.serve_forever()
