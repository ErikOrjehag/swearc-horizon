
import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
import numpy as np
from arduino.arduino import Arduino
from vision.button_detector import ButtonDetector

def main():
    capture_device = 0
    
    cap = cv2.VideoCapture(capture_device)

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
    arduino.send("light", True)    

    scale = 0.5
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

        if ellipse:
            cv2.ellipse(small, ellipse, (0, 255, 0), 3)
            xnow = ellipse[0][0] - small.shape[1] / 2

        x += (xnow - x) * 0.05
        
        cv2.line(small, (small.shape[1] / 2, small.shape[0] / 2), (int((small.shape[1] / 2) + x), small.shape[0] / 2), (255, 0, 0), 3)
        
        xnorm = min(1, max(-1, x / (small.shape[1] / 2)))

        speed = xnorm * 25 # rpm

        if counter % 10 == 0:
            arduino.send("lspeed", speed)
            arduino.send("rspeed", -speed)
            print(speed)

        cv2.imshow('frame', small)

        if keyboard == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
