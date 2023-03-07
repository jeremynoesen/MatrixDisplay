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

    def do_GET(self):
        """
        Process GET requests, which includes sending the web panel
        """
        global current_mode

        # GET the web UI
        if self.path == "/ui":

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            # Create image buttons
            files = os.listdir(config.pictures_dir)
            files.sort()
            links = ""
            scripts = ""
            for file in files:
                links += f'<a href=javascript:image{files.index(file)}()>{file}</a>, '
                scripts += f'<script>\n' + \
                           f'    function image{files.index(file)}() {{\n' + \
                           f'        fetch("/api", {{\n' \
                           f'            method: "POST",\n' \
                           f'            headers: {{\n' \
                           f'                         "Accept": "application/json",\n' \
                           f'                         "Content-Type": "application/json"\n' \
                           f'                     }},\n' \
                           f'            body: JSON.stringify({{mode: "image", image: "{file}"}})\n' \
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
        elif self.path == "/api":

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            # Write state as JSON
            data = {
                "mode": current_mode,
                "image": image.current_image,
                "display_time": slideshow.display_time,
                "color": color.current_color,
                "brightness": display.current_brightness,
                "warmth": display.current_warmth
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        """
        Process POST requests, which only updates the display
        """
        global current_mode

        if self.path == "/api":

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            # Read request data
            data = json.loads(self.rfile.read(int(self.headers.get('Content-Length'))))

            # Process request
            try:
                if "mode" in data.keys():
                    if data["mode"] == "image":
                        if "image" in data.keys():
                            sanitized = data["image"].replace("/", "").replace("..", "")
                            if os.path.exists(f'{config.pictures_dir}{sanitized}'):
                                current_mode = "image"
                                display.clear()
                                image.show(sanitized, True)
                            else:
                                current_mode = "off"
                                display.clear()

                    elif data["mode"] == "slideshow":
                        if "display_time" in data.keys():
                            current_mode = "slideshow"
                            display.clear()
                            slideshow.show(int(data["display_time"]))

                    elif data["mode"] == "color":
                        if "color" in data.keys():
                            current_mode = "color"
                            display.clear()
                            color.show(data["color"])

                    elif data["mode"] == "off":
                        current_mode = "off"
                        display.clear()

                if "brightness" in data.keys():
                    display.set_brightness(int(data["brightness"]))

                if "warmth" in data.keys():
                    display.set_warmth(int(data["warmth"]))

            except TypeError:
                current_mode = "off"
                display.clear()


def start():
    """
    Start the web control panel server
    """
    http_server = HTTPServer(("", 8080), Server)
    http_server.serve_forever()
