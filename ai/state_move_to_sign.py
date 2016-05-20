
import sys, os
sys.path.insert(0, os.path.abspath(".."))

from time import time
import cv2
from time import sleep
from calc.distance_calculator import DistanceCalculator
from vision.sign_detector import SignDetector


def state_move_to_sign(mega, kalman, template, sign_distance):

    distance_calculator = DistanceCalculator(distance_mm=400., size_px=75.)
    sign_detector = SignDetector(template)

    sent_speed_ts = [time()]
    minspeed = 8
    min_time = 5
    start_ts = [None]

    def inner(itr, fsm, frame):

        if itr == 0:
            start_ts[0] = time()

        print("move to sign")

        sign = sign_detector.find_sign(frame)

        print(sign)

        if sign:
            x = sign[0]
            cv2.circle(frame, (x, frame.shape[0] / 2), 10, (255, 255, 0), -1)
            x -= frame.shape[1] / 2
            height = sign[1]
            correct = cv2.cv.CreateMat(2, 1, cv2.cv.CV_32FC1)
            correct[0, 0] = x
            correct[1, 0] = height
            cv2.cv.KalmanCorrect(kalman, correct)

        prediction = cv2.cv.KalmanPredict(kalman)

        x = prediction[0, 0]
        height = prediction[1, 0]

        distance = distance_calculator.convert(height) if height else 1000

        print("x: " + str(x) + ", height: " + str(height) + ", distance: " + str(distance))

        cv2.line(frame, (frame.shape[1] / 2, frame.shape[0] / 2), (int((frame.shape[1] / 2) + x), frame.shape[0] / 2), (255, 0, 0), 3)

        distnorm = min(1, max(-1, (distance - 120) / 500))
        xnorm = min(1, max(-1, x / (frame.shape[1] / 2)))

        rspeed = lspeed = max(distnorm * 20, minspeed)

        if time() - sent_speed_ts[0] > 0.1:
            sent_speed_ts[0] = time()

            if distance > sign_distance or time() - start_ts[0] < min_time:
                mega.send("lspeed", lspeed + xnorm * 20)
                mega.send("rspeed", rspeed - xnorm * 20)
            else:
                mega.send("lspeed", 0)
                mega.send("rspeed", 0)
                sleep(0.5)
                fsm.pop_state()

    return inner

