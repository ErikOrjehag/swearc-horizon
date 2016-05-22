import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.button_detector import ButtonDetector
from ai.state_move_to_sign import state_move_to_sign
from vision.sign_detector import SignDetector
import config
import cv2
from time import time

west_template = cv2.imread("../vision/west.png")
east_template = cv2.imread("../vision/east.png")
north_template = cv2.imread("../vision/north.png")
south_template = cv2.imread("../vision/south.png")


def state_find_destination2(mega, kalman, destination):

    ts = [None]
    turn_time = [None]
    w_detector = SignDetector(west_template)
    e_detector = SignDetector(east_template)
    n_detector = SignDetector(north_template)
    s_detector = SignDetector(south_template)

    def inner(itr, fsm, frame):

        print("find destination 2")
        speed = 15
        sign_distance = 1500

        if itr == 0:
            ts[0] = time()
            mega.send("rspeed", -speed)
            mega.send("lspeed", speed)

        if destination[0] == "W":
            sign = w_detector.find_sign(frame)
            if sign:
                fsm.pop_state()
                fsm.push_state(state_move_to_sign(mega, kalman, west_template, sign_distance))
        elif destination[0] == "E":
            sign = e_detector.find_sign(frame)
            if sign:
                fsm.pop_state()
                fsm.push_state(state_move_to_sign(mega, kalman, east_template, sign_distance))
        elif destination[0] == "N":
            sign = n_detector.find_sign(frame)
            if sign:
                fsm.pop_state()
                fsm.push_state(state_move_to_sign(mega, kalman, north_template, sign_distance))
        elif destination[0] == "S":
            sign = s_detector.find_sign(frame)
            if sign:
                fsm.pop_state()
                fsm.push_state(state_move_to_sign(mega, kalman, south_template, sign_distance))

    return inner

