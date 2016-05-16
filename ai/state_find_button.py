import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.button_detector import ButtonDetector
import config
import cv2


def state_find_button(kalman, mega): 

    button_detector = ButtonDetector(config.btn_hsv_range)

    def inner(itr, fsm, frame):

        print("find button")

        if itr == 0:
            mega.send("rspeed", 10)
            mega.send("lspeed", 10)

        ellipse = button_detector.find_button(frame)

        if ellipse:
            mega.send("rspeed", 0)
            mega.send("lspeed", 0)

            fsm.pop_state()

            x = ellipse[0][0] - frame.shape[1] / 2
            height = ellipse[1][1]
            correct = cv2.cv.CreateMat(2, 1, cv2.cv.CV_32FC1)
            correct[0, 0] = x
            correct[1, 0] = height
            cv2.cv.KalmanCorrect(kalman, correct)

    return inner
