## Installation

# alphabot-interface

![AlphaBot](https://i.imgur.com/JLBU5cs.png)

**Version:** 0.1.1  
**Author:** @sadra-hub on GitHub
**License:** MIT  
**Python Version:** 3.8+

---

## Description

`alphabot-interface` provides a modular and simple Python interface for interacting with key components of the [Waveshare AlphaBot 2](https://www.waveshare.com/wiki/AlphaBot2) platform, including:

- **Camera** module (using Picamera2)
- **Battery** monitoring
- **Motor** control

`alphabot-interface` is a lightweight Python package that lets you **comfortably use various components of the AlphaBot platform** and write **clean, readable, and modular code**.

This package is designed to abstract hardware-level interactions so developers and students can focus on high-level robotics programming.

---

## Installation

You can install the package via `pip` after publishing it to PyPI:

```bash
pip install alphabot-interface
```

## Usage

This package let you comfortably use various components of AlphaBot and write clean, readable code. 


```python
from alphabot_interface import Camera, Battery, Motor

# Initialize components
camera = Camera()
battery = Battery()
motor = Motor()

# Use the motor
motor.forward()
battery_status = battery.get_status()

# Take a photo with camera and save it to output.jpg
camera.take_picture("output.jpg")
```