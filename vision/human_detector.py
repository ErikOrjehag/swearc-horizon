
from __future__ import print_function
from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2


class HumanDetector:

    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def find_human(self, frame):

        scale = 2.
        fram = cv2.resize(frame, (0, 0), fx=1./scale, fy=1./scale)

        # detect people in the image
        rects, weights = self.hog.detectMultiScale(fram, winStride=(4, 4), padding=(32, 32), scale=1.05)

        li = []
        # draw the original bounding boxes
        for i in range(0, len(rects)):
            weight = weights[i]
            rect = rects[i]
            x, y, w, h = rect
            if weight >= 1:
                cv2.rectangle(fram, (x, y), (x + w, y + h), (0, 0, 255), 3)
                li.append(rect)

        rect = np.array([[x, y, x + w, y + h] for (x, y, w, h) in li])
        pick = non_max_suppression(rect, probs=None, overlapThresh=0.65)

        human = None

        # draw the final bounding boxes
        for xA, yA, xB, yB in pick:
            xA *= scale
            yA *= scale
            xB *= scale
            yB *= scale
            cv2.rectangle(frame, (int(xA), int(yA)), (int(xB), int(yB)), (0, 255, 0), 1)
            height = yB - yA
            x = (xA + xB) / 2.
            if human is None or height > human[1]:
                human = [x, height]

        # frame2 = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
        # cv2.imshow("After NMS", frame2)
        cv2.imshow("fram", fram)


        return human


