<img src="img/Logo.svg" alt="Logo" title = "Logo" align="right" width="200" height="200" />


# MatrixDisplay

## About
MatrixDisplay is a Python program used to display images on the Pimoroni Unicorn HAT for Raspberry Pi through a web interface.

## Purpose
This project exists mainly as a way for me to try a new programming language, as well as to create a project that has both software and hardware aspects in it. I also just wanted to make my own smart home gadget.

## Usage
### Web Interface
On the same network as the Raspberry Pi, open your browser to `http://yourpihostname.local:8080/ui`. From there, you can control the display output from a web interface.

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
- [Pibow Ninja](https://shop.pimoroni.com/products/pibow-for-raspberry-pi-3-b-plus?variant=2601126395914) case (optional)
- [Pibow Ninja diffuser](https://shop.pimoroni.com/products/pibow-modification-layers?variant=1047619725) Pibow modification layer (optional)
- Micro USB cable for power
- Micro SD card

## Installation
### Manual
Clone or download this repository onto the Raspberry Pi.

### Systemd
1. Clone or download this repository onto the Raspberry Pi.
2. Create the following `matrixdisplay.service` file in `/etc/systemd/system/`, making sure to change the `WorkingDirectory` and `ExecStart`, as well as the `User`:
```ini
[Unit]
Description=Matrix Display Program
After=network-online.target

[Service]
WorkingDirectory=/path/to/MatrixDisplay/
ExecStart=/usr/bin/sudo /usr/bin/python3 /path/to/main.py
User=set_user_here
Type=simple
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Running
### Manual
Run `sudo python3 /path/to/main.py`.

### Systemd
Run `sudo systemctl enable matrixdisplay && sudo systemctl start matrixdisplay` to start the service and set it to run at boot.

## Configuration
There are two configurable values located in `config.py`:
- `pictures_dir`: The location of the directory where images are stored.
- `cache_dir`: The location of the directory where cached images will be saved.

## Home Assistant
This project can be added to Home Assistant using the RESTful Switch integration. The following is an example entry in `configuration.yaml` to add a switch to Home Assistant that turns the display on to slideshow mode with set brightness and warmth, as well as turn it off:
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
