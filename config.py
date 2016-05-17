import numpy as np

capture_device = 0

mega_usb = "/dev/ttyUSB1"
nano_usb = "/dev/ttyUSB0"

btn_hsv_range = np.array([[
    [130, 80, 100],
    [255, 255, 255]
], [
    [0, 80, 100],
    [30, 255, 255]
]])