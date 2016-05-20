
import sys, os
sys.path.insert(0, os.path.abspath(".."))

from vision.human_detector import HumanDetector
from time import time
import cv2
from time import sleep


def state_move_to_human(mega, kalman):

    human_detector = HumanDetector()

    start_ts = [None]
    sent_speed_ts = [time()]
    minspeed = 5
    min_time = 8

    def inner(itr, fsm, frame):

        if itr == 0:
            start_ts[0] = time()

        human = human_detector.find_human(frame)

        if human:

            correct = cv2.cv.CreateMat(2, 1, cv2.cv.CV_32FC1)
            correct[0, 0] = human[0] - frame.shape[1] / 2
            correct[1, 0] = human[1]
            cv2.cv.KalmanCorrect(kalman, correct)

        prediction = cv2.cv.KalmanPredict(kalman)

        x = prediction[0, 0]
        height = prediction[1, 0]

        ratio = float(height) / float(frame.shape[0])

        print("x: " + str(x) + ", height: " + str(height) + ", ratio: " + str(ratio))

        cv2.line(frame, (frame.shape[1] / 2, frame.shape[0] / 2), (int((frame.shape[1] / 2) + x), frame.shape[0] / 2), (255, 0, 0), 3)

        xnorm = min(1, max(-1, x / (frame.shape[1] / 2)))

        rspeed = lspeed = max(10, minspeed)

        if time() - sent_speed_ts[0] > 0.1:
            sent_speed_ts[0] = time()

            if ratio < 0.85 or time() - start_ts[0] < min_time:
                mega.send("lspeed", lspeed + xnorm * 10)
                mega.send("rspeed", rspeed - xnorm * 10)
            else:
                mega.send("lspeed", 0)
                mega.send("rspeed", 0)
                sleep(0.5)
                fsm.pop_state()

    return inner

