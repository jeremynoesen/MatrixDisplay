from http.server import BaseHTTPRequestHandler

import image
import filter
from PIL import Image


class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        html = """
            <html>
            <body>
            <h1>Pi Matrix Display Control Panel</h1>
            <p><a href="/test1">SHOW</a> <a href="/test2">HIDE</a></p>
            </body>
            </html>
        """
        self.do_HEAD()
        if self.path == '/test1':
            image.show_image(Image.open("/home/pi/Pictures/troll.png"))
        elif self.path == '/test2':
            filter.set_warmth(30)
        self.wfile.write(html.encode("utf-8"))
