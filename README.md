# MatrixDisplay

## About
MatrixDIsplay is a Python program used to display images on the Pimoroni Unicorn HAT for Raspberry Pi through a web interface.

## Purpose
This project exists mainly as a way for me to try a new programming language, as well as to create a project that has both software and hardware aspects in it.

## Usage
On the same Wi-Fi network as the Raspberry Pi, open your browser to `https://yourpihostname.local:8080`. From there, you can control the display output.

## Requirements
Software:
- Python 3 or higher
- The [unicorn-hat](https://github.com/pimoroni/unicorn-hat) library from Pimoroni
- The [Pillow](https://pypi.org/project/Pillow/) library

Hardware:
- A Raspberry Pi with the 40-pin header
- The [Pimoroni Unicorn HAT](https://shop.pimoroni.com/products/unicorn-hat)
- A [Pibow Ninja](https://shop.pimoroni.com/products/pibow-for-raspberry-pi-3-b-plus?variant=2601126395914) case (optional)
- A [Pibow Ninja diffuser](https://shop.pimoroni.com/products/pibow-modification-layers?variant=1047619725) Pibow modification layer (optional)
- A micro USB cable for power
- A Micro SD card

## Installation
To install, simply clone the repo onto the Raspberry Pi, and set `main.py` to start when the Pi turns on.

## Running
To run the program, open a terminal and type `sudo python3 /path/to/main.py`. Replace the path to main.py with the proper location to your installation's main.py.

## Configuration
The only configurable value is the path to the images folder. In `server/server.py` you can set `pictures_dir` to your own images directory.

## Demonstration
Demonstrations will be added soon!

## Troubleshooting
This is also coming soon.