<img src="img/Logo.svg" alt="Logo" title="Logo" align="right" width="72" height="72" />

# MatrixDisplay

## About

MatrixDisplay is a Python program used to display images on the Pimoroni Unicorn HAT for Raspberry Pi through a web
interface.

## Purpose

This project exists mainly as a way for me to try a new programming language, as well as to create a project that has
both software and hardware aspects in it. I also just wanted to make my own smart home gadget.

## Usage

### Web Interface

On the same network as the Raspberry Pi, open your browser to `http://yourpihostname.local:8080/ui`. From there, you can
control the display output from a web interface. Note that this page does not automatically refresh; it only updates
when you click something or manually refresh the page.

<div align="center" ><img src="img/webinterface.png" alt="Example Web Interface" title="Example Web Interface" /></div>

### API

This API is used by the web interface, but can also be used by other programs to control the display.

#### GET

- `http://DISPLAY-IP:8080/ui`: Get web interface HTML
- `http://DISPLAY-IP:8080/api`: Get device state as JSON

#### POST

- `http://DISPLAY-IP:8080/api`: Set device state with JSON

#### JSON Format

```json
{
  "mode": "off",
  "image": "image.png",
  "display_time": 0,
  "color": "000000",
  "brightness": 100,
  "warmth": 0
}
```

- `mode`: `image`, `slideshow`, `color`, or `off`
- `image`: Image file name
- `display_time`: Display time for slideshow in seconds
- `color`: Color for color mode in hex
- `brightness`: Display brightness as a percent
- `warmth`: Display warmth as a percent

## Requirements

### Software:

- Python 3
- [unicorn-hat](https://github.com/pimoroni/unicorn-hat) library
- [Pillow](https://pypi.org/project/Pillow/) library

### Hardware:

- Raspberry Pi with the 40-pin header
- [Pimoroni Unicorn HAT](https://shop.pimoroni.com/products/unicorn-hat)
- [Pibow Ninja](https://shop.pimoroni.com/products/pibow-for-raspberry-pi-3-b-plus?variant=2601126395914) case (
  optional)
- [Pibow Ninja diffuser](https://shop.pimoroni.com/products/pibow-modification-layers?variant=1047619725) Pibow
  modification layer (optional)
- Micro USB cable for power
- Micro SD card

## Installation

1. Install Python 3.
2. Clone or download this repository onto the Raspberry Pi.
3. Run `pip3 install -r requirements.txt`.
4. If using Systemd to auto-start the program, Create the following `matrixdisplay.service` file
   in `/etc/systemd/system/`, making sure to change the `WorkingDirectory` and `ExecStart`, as well as the `User`:

```ini
[Unit]
Description = MatrixDisplay Program
After = network-online.target

[Service]
WorkingDirectory = /path/to/MatrixDisplay/
ExecStart = /usr/bin/sudo /usr/bin/python3 /path/to/main.py
User = set_user_here
Type = simple
Restart = on-failure

[Install]
WantedBy = multi-user.target
```

## Running

### Manual

Run `sudo python3 /path/to/main.py`.

### Systemd

Run `sudo systemctl enable matrixdisplay && sudo systemctl start matrixdisplay` to start the service and set it to run
at boot.

## Configuration

There are two configurable values located in `config.py`:

- `pictures_dir`: The location of the directory where images are stored. This directory should only contain images and
  no hidden files.
    - When adding images to this directory, you must refresh the web interface for the images list to
      update.
    - If running the slideshow, you must restart the slideshow mode for the new images to show up.
- `cache_dir`: The location of the directory where cached images will be saved.
    - If an image is ever modified in the
      pictures directory, remove the corresponding file from this directory to have it be regenerated.

## Updating

1. Re-download or git pull (if you cloned) this repository.
2. Run `pip3 install -r requirements.txt` to install any new requirements.
3. Restart the program. (If using systemd, run `sudo systemctl restart matrixdisplay`).

## Home Assistant

This project can be added to Home Assistant using the RESTful Switch integration. The following is an example entry
in `configuration.yaml` to add a switch to Home Assistant that turns the display on to slideshow mode with set
brightness and warmth, as well as turn it off:

```yaml
switch:
  - platform: rest
    resource: http://DISPLAY-IP:8080/api
    body_on: '{"mode": "slideshow", "display_time": 60, "brightness": 40, "warmth": 20}'
    body_off: '{"mode": "off"}'
    is_on_template: '{{ value_json.mode != "off" }}'
    headers:
      Content-Type: application/json
    verify_ssl: false
    name: matrix_display
```

## Demonstration

[Watch on YouTube](https://youtu.be/zxgAzgMzVN0)
