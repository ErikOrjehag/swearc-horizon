import sys, os
sys.path.insert(0, os.path.abspath(".."))
from calc.distance_calculator import DistanceCalculator
from vision.button_detector import ButtonDetector
from time import time
import config
import cv2
from time import sleep


def state_move_to_button(kalman, mega, nano, dist_to_btn):

    distance_calculator = DistanceCalculator(distance_mm=250., size_px=207.)
    button_detector = ButtonDetector(config.btn_hsv_range)

    start_ts = [None]
    sent_speed_ts = [time()]
    minspeed = 8
    min_time = 5

    def inner(itr, fsm, frame):

        if itr == 0:
            start_ts[0] = time()

        ellipse = button_detector.find_button(frame)

        if ellipse:
            cv2.ellipse(frame, ellipse, (0, 255, 0), 3)
            x = ellipse[0][0] - frame.shape[1] / 2
            height = ellipse[1][1]
            correct = cv2.cv.CreateMat(2, 1, cv2.cv.CV_32FC1)
            correct[0, 0] = x
            correct[1, 0] = height
            cv2.cv.KalmanCorrect(kalman, correct)

        prediction = cv2.cv.KalmanPredict(kalman)

        x = prediction[0, 0]
        height = prediction[1, 0]

        distance = distance_calculator.convert(height) if height else 1000

        cv2.line(frame, (frame.shape[1] / 2, frame.shape[0] / 2), (int((frame.shape[1] / 2) + x), frame.shape[0] / 2), (255, 0, 0), 3)

        distnorm = min(1, max(-1, (distance - 120) / 500))
        xnorm = min(1, max(-1, x / (frame.shape[1] / 2)))

        rspeed = lspeed = max(distnorm * 10, minspeed)

        print(distance)

        if time() - sent_speed_ts[0] > 0.1:
            sent_speed_ts[0] = time()

            if distance > dist_to_btn or time() - start_ts[0] < min_time:
                mega.send("lspeed", lspeed + xnorm * 10)
                mega.send("rspeed", rspeed - xnorm * 10)

            else:
                fsonar = mega.get("fsonar")
                print("check sonar: " + str(fsonar))
                if fsonar < dist_to_btn * 2:
                    print("OK!")
                    mega.send("lspeed", 0)
                    mega.send("rspeed", 0)
                    sleep(0.5)
                    fsm.pop_state()

    return inner


