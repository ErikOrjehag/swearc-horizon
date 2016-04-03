import sys
import cv2
import numpy as np


def main():

    template = cv2.imread(sys.argv[1])
    template = cv2.resize(template, (0, 0), fx=0.2, fy=0.2)
    th, tw = template.shape[:2]

    cap = cv2.VideoCapture(0)

    cv2.imshow("template", template)

    while True:

        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        threshold = 0.92
        # loc = np.where(result >= threshold)
        # for pt in zip(*loc[::-1]):
        #    cv2.rectangle(frame, pt, (pt[0] + tw, pt[1] + th), (0, 0, 255), 2)

        for scale in np.arange(1, 0.1, -0.1):

            result = cv2.matchTemplate(cv2.resize(frame, (0, 0), fx=scale, fy=scale), template, cv2.TM_CCORR_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > threshold:
                top_left = (int(max_loc[0] / scale), int(max_loc[1] / scale))
                bottom_right = (int(top_left[0] + tw / scale), int(top_left[1] + th / scale))
                cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 1)
                cv2.putText(frame, str(max_val), (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                break

        while True:
            keyboard = cv2.waitKey(10)
            if keyboard == ord("q"):
                exit()
            elif keyboard == ord(" ") or True:
                break

        cv2.imshow("result", frame)

if __name__ == "__main__":
    main()
