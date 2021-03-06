# MatrixDisplay

## About
MatrixDisplay is a Python program used to display images on the Pimoroni Unicorn HAT for Raspberry Pi through a web interface.

## Purpose
This project exists mainly as a way for me to try a new programming language, as well as to create a project that has both software and hardware aspects in it.

## Usage
On the same Wi-Fi network as the Raspberry Pi, open your browser to `http://yourpihostname.local:8080`. From there, you can control the display output from a web interface.

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
1. Clone or download this repository onto the Raspberry Pi.
2. Set `main.py` to start when the Pi turns on.

An installation script will be coming soon!

## Running
1. Open a terminal.
2. Run `sudo python3 /path/to/main.py`.

## Configuration
There are two configurable values located in `config.py`:
- `pictures_dir`: The location of the directory where images are stored.
- `cache_dir`: The location of the directory where cached images will be saved.

## Demonstration
Demonstrations will be added soon!

## Troubleshooting
This is also coming soon.