import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
import numpy as np
from vision.button_detector import ButtonDetector
import config


class DistanceCalculator:
    def __init__(self, distance_mm, size_px):
        self.size_px = size_px
        self.distance_mm = distance_mm

    def convert(self, px):
        return (self.size_px * self.distance_mm) / px


def main():
    capture_device = 0
    cap = cv2.VideoCapture(capture_device)

    distCalc = DistanceCalculator(distance_mm=250., size_px=207.)

    hsv_range = np.array(config.btn_hsv_range)

    buttonDetector = ButtonDetector(hsv_range)

    scale = 1
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    while True:

        # Input
        keyboard = cv2.waitKey(1)

        if keyboard & 0xFF == ord(' ') or True:
            ret, frame = cap.read()
            frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        ellipse = buttonDetector.find_button(frame)

        if ellipse:
            # print ellipse
            cv2.ellipse(frame, ellipse, (0, 0, 0), 3)
            pos = (int(ellipse[0][0]), int(ellipse[0][1]))
            # print pos
            # cv2.line(frame, (0, 0), pos, (0, 255, 0), 3)
            height = ellipse[1][1]
            width = ellipse[1][0]
            height_line = (int(pos[0]), int(pos[1] + height / 2.))
            width_line = (int(pos[0] + width / 2.), int(pos[1]))
            cv2.line(frame, pos, height_line, (255, 255, 255), 2)
            cv2.line(frame, pos, width_line, (255, 255, 255), 2)

            distance = distCalc.convert(height)
            print(height)

            #print distance
            #print diameter
            cv2.putText(frame, "distance: " + str(int(distance)) + " mm", (pos[0], pos[1] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            cv2.putText(frame, "angle: " + str(int(90 - (width / height) * 90)) + " deg", (pos[0], pos[1] - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

        cv2.imshow('original', frame)

        if keyboard & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
