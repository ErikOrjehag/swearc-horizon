import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.button_detector import ButtonDetector
import config
import cv2
from time import sleep, time


def state_find_button_turn(kalman, mega):

    button_detector = ButtonDetector(config.btn_hsv_range)
    ts = [0]

    def inner(itr, fsm, frame):

        print("find button turn")

        if itr == 0:
            mega.send("servo", 90)
            mega.send("rspeed", 15)
            mega.send("lspeed", -15)
            ts[0] = time()

        ellipse = button_detector.find_button(frame)

        if ellipse:

            x = ellipse[0][0] - frame.shape[1] / 2

            print(x)

            if x > -280 and time() - ts[0] > 3:
                mega.send("rspeed", 0)
                mega.send("lspeed", 0)
                sleep(1)

                fsm.pop_state()

    return inner
