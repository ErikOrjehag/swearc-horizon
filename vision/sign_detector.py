import cv2
import numpy as np
import math


class SignDetector():

    def __init__(self, template):
        self.template = cv2.resize(template, (0, 0), fx=0.2, fy=0.2)
        self.th, self.tw = self.template.shape[:2]

    def find_sign(self, image):

        cv2.imshow("template", self.template)

        sign = None

        threshold = 0.92
        # loc = np.where(result >= threshold)
        # for pt in zip(*loc[::-1]):
        #    cv2.rectangle(frame, pt, (pt[0] + tw, pt[1] + th), (0, 0, 255), 2)

        for scale in np.arange(0.4, 0, -0.05):

            result = cv2.matchTemplate(cv2.resize(image, (0, 0), fx=scale, fy=scale), self.template, cv2.TM_CCORR_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > threshold:
                top_left = (int(max_loc[0] / scale), int(max_loc[1] / scale))
                bottom_right = (int(top_left[0] + self.tw / scale), int(top_left[1] + self.th / scale))
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 1)
                cv2.putText(image, str(max_val), (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                x = (bottom_right[0] + top_left[0]) / 2
                height = bottom_right[1] - top_left[1]
                sign = (x, height)
                break

        cv2.imshow("result", image)

        return sign
