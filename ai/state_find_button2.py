import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.button_detector import ButtonDetector
import config
import cv2
from time import sleep


def state_find_button2(kalman, mega):

    button_detector = ButtonDetector(config.btn_hsv_range)

    def inner(itr, fsm, frame):

        print("find button")

        if itr == 0:
            mega.send("rspeed", 10)
            mega.send("lspeed", 10)

        ellipse = button_detector.find_button(frame)

        if ellipse:

            x = ellipse[0][0] - frame.shape[1] / 2

            if x < -200:
                mega.send("rspeed", 10)
                mega.send("lspeed", 10)
                sleep(7.5)
                #mega.send("rspeed", 15)
                #mega.send("lspeed", -15)
                #sleep(8)
                #mega.send("rspeed", 10)
                #mega.send("lspeed", 10)
                #sleep(5)
                mega.send("rspeed", 0)
                mega.send("lspeed", 0)
                sleep(1)

                fsm.pop_state()

    return inner
