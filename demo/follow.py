
import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
import numpy as np
from arduino.arduino import Arduino
from vision.button_detector import ButtonDetector
from vision.distance import DistanceCalculator

def main():
    capture_device = 0
    
    cap = cv2.VideoCapture(capture_device)
    #cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)

    hsv_range = np.array([[
        [130, 80, 100],
        [255, 255, 255]
    ], [
        [0, 80, 100],
        [30, 255, 255]
    ]])
    """hsv_range = np.array([[
        [0, 0, 0],
        [255, 50, 50]
    ]])"""

    button_detector = ButtonDetector(hsv_range)
    arduino = Arduino("/dev/ttyUSB0")
    distCalc = DistanceCalculator(distance_mm=250., size_px=207.)

    scale = 1.0
    x = 0
    counter = 0

    while True:

        counter += 1

        # Input
        keyboard = cv2.waitKey(1) & 0xFF

        ret, frame = cap.read()

        small = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        ellipse = button_detector.find_button(small)

        xnow = 0
        znorm = 0

        if ellipse:
            cv2.ellipse(small, ellipse, (0, 255, 0), 3)
            xnow = ellipse[0][0] - small.shape[1] / 2
            height = ellipse[1][1]
            distance = distCalc.convert(height)
            znorm = min(1, max(-1, (distance - 120) / 500))
            print(znorm)

        x += (xnow - x) * 0.05
        
        cv2.line(small, (small.shape[1] / 2, small.shape[0] / 2), (int((small.shape[1] / 2) + x), small.shape[0] / 2), (255, 0, 0), 3)
        
        xnorm = min(1, max(-1, x / (small.shape[1] / 2)))

        rspeed = lspeed = znorm * 20 # rpm
        rspeed -= xnorm * 20
        lspeed += xnorm * 20

        if counter % 20 == 0:
            arduino.send("lspeed", lspeed)
            arduino.send("rspeed", rspeed)

        cv2.imshow('frame', small)

        if keyboard == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
