
import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.detect_qr_code import DetectQRCode
import json
from time import time
import pyttsx
import cv2
from time import sleep
from calc.distance_calculator import DistanceCalculator


def state_move_to_bag(mega, kalman, destination, bag_distance):

    qr_detector = DetectQRCode()
    distance_calculator = DistanceCalculator(distance_mm=500., size_px=140.)

    start_ts = [None]
    sent_speed_ts = [time()]
    minspeed = 5
    min_time = 5

    def inner(itr, fsm, frame):

        if itr == 0:
            start_ts[0] = time()

        symbol = qr_detector.detect_qr(frame)

        if symbol:

            if not destination[0]:
                print(symbol.data)
                destination[0] = json.loads(symbol.data)["destination"]

            cv2.circle(frame, symbol.location[0], 5, (0, 0, 255), -1)
            cv2.circle(frame, symbol.location[1], 5, (0, 255, 0), -1)
            cv2.circle(frame, symbol.location[2], 5, (255, 0, 0), -1)
            cv2.circle(frame, symbol.location[3], 5, (0, 255, 255), -1)

            pos = [0, 0]
            for point in symbol.location:
                pos[0] += point[0]
                pos[1] += point[1]
            pos[0] /= 4
            pos[1] /= 4
            cv2.circle(frame, tuple(pos), 10, (255, 255, 0), -1)
            pos[0] -= frame.shape[1] / 2

            height = symbol.location[0][1] - symbol.location[3][1]

            correct = cv2.cv.CreateMat(2, 1, cv2.cv.CV_32FC1)
            correct[0, 0] = pos[0]
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

        rspeed = lspeed = max(distnorm * 10, minspeed)

        if time() - sent_speed_ts[0] > 0.1:
            sent_speed_ts[0] = time()

            if distance > bag_distance or time() - start_ts[0] < min_time:
                mega.send("lspeed", lspeed + xnorm * 10)
                mega.send("rspeed", rspeed - xnorm * 10)
            else:
                mega.send("lspeed", 0)
                mega.send("rspeed", 0)
                sleep(0.5)
                fsm.pop_state()

    return inner

