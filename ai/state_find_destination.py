import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.button_detector import ButtonDetector
from ai.state_move_to_sign import state_move_to_sign
import config
import cv2
from time import time

west_template = cv2.imread("../vision/west.png")
east_template = cv2.imread("../vision/east.png")
north_template = cv2.imread("../vision/north.png")
south_template = cv2.imread("../vision/south.png")


def state_find_destination(mega, kalman, destination):

    ts = [None]
    turn_time = [None]

    def inner(itr, fsm, frame):

        print("find destination")
        turn_90_time = 8.5
        speed = 15
        sign_distance = 350

        if itr == 0:
            ts[0] = time()
            if destination[0] == "W":
                mega.send("rspeed", -speed)
                mega.send("lspeed", speed)
                turn_time[0] = turn_90_time
            elif destination[0] == "E":
                mega.send("rspeed", speed)
                mega.send("lspeed", -speed)
                turn_time[0] = turn_90_time
            elif destination[0] == "N":
                mega.send("rspeed", speed)
                mega.send("lspeed", -speed)
                turn_time[0] = turn_90_time * 2
            elif destination[0] == "S":
                turn_time[0] = 0

        if time() - ts[0] > turn_time[0]:
            mega.send("rspeed", 0)
            mega.send("lspeed", 0)

            fsm.pop_state()

            if destination[0] == "W":
                fsm.push_state(state_move_to_sign(mega, kalman, west_template, sign_distance))
            elif destination[0] == "E":
                fsm.push_state(state_move_to_sign(mega, kalman, east_template, sign_distance))
            elif destination[0] == "N":
                fsm.push_state(state_move_to_sign(mega, kalman, north_template, sign_distance))
            elif destination[0] == "S":
                fsm.push_state(state_move_to_sign(mega, kalman, south_template, sign_distance))

    return inner

