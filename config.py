import numpy as np

capture_device = 0

mega_usb = "/dev/ttyUSB1"
nano_usb = "/dev/ttyUSB0"

btn_hsv_range = np.array([[
    [150, 80, 50],
    [255, 255, 255]
], [
    [0, 80, 50],
    [30, 255, 255]
]])

"""
btn_hsv_range = np.array([[
    [230, 180, 150],
    [255, 255, 255]
], [
    [0, 80, 50],
    [20, 255, 255]
]])
"""

seat_hsv_range = np.array([[
    [60, 80, 100],
    [220, 255, 255]
]])