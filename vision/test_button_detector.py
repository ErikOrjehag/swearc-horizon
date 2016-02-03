

import numpy as np
import cv2
import cv2.cv
import sys
import time
from button_detector import ButtonDetector


def get_hsv_range():
    huel = cv2.getTrackbarPos("Hue_Lower", 'image')
    satl = cv2.getTrackbarPos("Sat_Lower", 'image')
    vil = cv2.getTrackbarPos("Vi_Lower", 'image')
    hueu = cv2.getTrackbarPos("Hue_Upper", 'image')
    satu = cv2.getTrackbarPos("Sat_Upper", 'image')
    viu = cv2.getTrackbarPos("Vi_Upper", 'image')
    hsv_range = np.array([
        [huel, satl, vil],
        [hueu, satu, viu]
    ])
    return hsv_range


def main():

    capture_device = 0

    if "--video" in sys.argv:
        capture_device = "ticket_button.mp4"

    cap = cv2.VideoCapture(capture_device)

    hsv_range = np.array([
        [0, 115, 115],
        [15, 255, 255]
    ])

    if "--ticket" in sys.argv:
        hsv_range = np.array([
            [0, 115, 157],
            [15, 255, 216]
        ])

    button_detector = ButtonDetector(hsv_range)

    def trackbar_cb(x):
        new_hsv_range = get_hsv_range()
        print(new_hsv_range)
        button_detector.set_hsv_range(new_hsv_range)

    cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Hue_Lower", 'image', hsv_range[0][0], 255, trackbar_cb)
    cv2.createTrackbar("Hue_Upper", 'image', hsv_range[1][0], 255, trackbar_cb)
    cv2.createTrackbar("Sat_Lower", 'image', hsv_range[0][1], 255, trackbar_cb)
    cv2.createTrackbar("Sat_Upper", 'image', hsv_range[1][1], 255, trackbar_cb)
    cv2.createTrackbar("Vi_Lower", 'image', hsv_range[0][2], 255, trackbar_cb)
    cv2.createTrackbar("Vi_Upper", 'image', hsv_range[1][2], 255, trackbar_cb)


    startTime = time.time()
    prevTime = None

    scale = 0.5
    ret, frame = cap.read()
    small = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

    while True:

        # Input
        keyboard = cv2.waitKey(1)

        # FPS
        nowTime = time.time()
        if prevTime:
            print("%3d fps" % (1 / (nowTime - prevTime)))
        prevTime = nowTime

        # Capture frame-by-frame
        if keyboard & 0xFF == ord(' ') or True:
            ret, frame = cap.read()

        small = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        ellipse = button_detector.find_button(small)

        # TODO: Create a filter that looks at the sequence of
        # TODO: button positions reduce effects of drastic change,
        # TODO: likely caused by a mistake of the detector.

        if ellipse:
            cv2.ellipse(small, ellipse, (0, 255, 0), 3)

        cv2.imshow('original', small)

        if keyboard & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
