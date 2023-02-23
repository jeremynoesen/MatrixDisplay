"""
A simple web server and interface used to easily control the Unicorn HAT
"""
import json
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
        global current_mode

        # GET the web UI
        if (self.path == "/ui"):
            # Headers
            self.do_HEAD()

            # Create image buttons
            files = os.listdir(config.pictures_dir)
            files.sort()
            links = ""
            scripts = ""
            for file in files:
                links += f'<a href=javascript:image{files.index(file)}()>{file}</a>, '
                scripts += f'<script>\n' + \
                           f'    function image{files.index(file)}() {{\n' + \
                           f'        fetch("/api" + this.value, {{\n' \
                           f'            method: "POST",\n' \
                           f'            headers: {{\n' \
                           f'                         "Accept": "application/json",\n' \
                           f'                         "Content-Type": "application/json"\n' \
                           f'                     }},\n' \
                           f'            body: JSON.stringify({{mode: "image", image: {file}}})\n' \
                           f'        }});\n' \
                           f'        document.getElementById("imagetitle").textContent = "> Image: {file}";\n' + \
                           f'        document.getElementById("slideshowtitle").textContent = "- Slideshow";\n' + \
                           f'        document.getElementById("colortitle").textContent = "- Color";\n' + \
                           f'        document.getElementById("offtitle").textContent = "- Off";\n' + \
                           f'        document.getElementById("slideshowdisplaytime").value = 0;\n' \
                           f'        document.getElementById("colorpicker").value = "#000000";\n' \
                           f'    }}\n' + \
                           f'</script>\n'

            # Fill in HTML placeholders
            with open("./server/index.html") as fd:
                data = fd.read().replace("{links}", links.removesuffix(", ")) \
                    .replace("{scripts}", scripts) \
                    .replace("{display_time}", str(slideshow.display_time)) \
                    .replace("{color}", color.current_color) \
                    .replace("{brightness}", str(display.current_brightness)) \
                    .replace("{warmth}", str(display.current_warmth)) \
                    .replace("{brightnesstitle}", f"- Brightness {display.current_brightness}%") \
                    .replace("{warmthtitle}", f"- Warmth {display.current_warmth}%")

                if current_mode == "image":
                    data = data.replace("{imagetitle}", f"> Image: {image.current_image}")
                elif current_mode == "slideshow":
                    data = data.replace("{slideshowtitle}", f"> Slideshow: {slideshow.display_time} seconds per image")
                    data = data.replace("{imagetitle}", f"- Image: {image.current_image}")
                elif current_mode == "color":
                    data = data.replace("{colortitle}", f"> Color: #{color.current_color}")
                elif current_mode == "off":
                    data = data.replace("{offtitle}", "> Off")

                data = data.replace("{imagetitle}", "- Image") \
                    .replace("{slideshowtitle}", "- Slideshow") \
                    .replace("{colortitle}", "- Color") \
                    .replace("{offtitle}", "- Off")
                self.wfile.write(data.encode("utf-8"))

        # GET the state of the device
        elif (self.path == "/api"):
            # Headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Write state as JSON
            data = f'{{' \
                   f'"mode": "{current_mode}", ' \
                   f'"image": "{image.current_image}", ' \
                   f'"display_time": {slideshow.display_time}, ' \
                   f'"color": "{color.current_color}", ' \
                   f'"brightness": {display.current_brightness}, ' \
                   f'"warmth": {display.current_warmth}' \
                   f'}}'
            self.wfile.write(data.encode("utf-8"))


    def do_POST(self):
        """
        Process POST requests, which only updates the display
        """
        global current_mode

        if self.path == "/api":
            # Headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Read request data
            data: dict = json.loads(self.rfile.read().decode("utf-8"))

            # Process request
            try:
                if data.__contains__("mode"):
                    if data["mode"] == "image":
                        if data.__contains__("image"):
                            if os.path.exists(f'{config.cache_dir}{data["image"]}.pickle") or \
                                    os.path.exists(f"{config.pictures_dir}{data["image"]}'):
                                current_mode = "image"
                                display.clear()
                                image.show(data["image"], True)
                            else:
                                current_mode = "off"
                                display.clear()

                    elif data["mode"] == "slideshow":
                        if data.__contains__("display_time"):
                            current_mode = "slideshow"
                            display.clear()
                            slideshow.show(data["display_time"])

                    elif data["mode"] == "color":
                        if data.__contains__("color"):
                            current_mode = "color"
                            display.clear()
                            color.show(data["color"])

                    elif data["mode"] == "off":
                        current_mode = "off"
                        display.clear()

                if data.__contains__("brightness"):
                    display.set_brightness(data["brightness"])

                if data.__contains__("warmth"):
                    display.set_warmth(data["warmth"])

            except TypeError:
                current_mode = "off"
                display.clear()


def start():
    """
    Start the web control panel server
    """
    http_server = HTTPServer(("", 8080), Server)
    http_server.serve_forever()
