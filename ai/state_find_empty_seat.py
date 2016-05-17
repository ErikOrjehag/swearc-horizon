import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.seat_detector import SeatDetector
import config
from time import time


def state_find_empty_seat(mega):

    detector = SeatDetector(config.seat_hsv_range)
    has_seen_far = [False]
    has_seen_near = [False]
    ts = [None]

    def inner(itr, fsm, frame):

        if itr == 0:
            mega.send("lspeed", 10)
            mega.send("rspeed", 10)

        if not has_seen_far[0]:
            distance = mega.get("fsonar")
            if distance and distance > 400:
                has_seen_far[0] = True
        elif not has_seen_near[0]:
            distance = mega.get("fsonar")
            if distance and distance < 400:
                has_seen_far[0] = True
                ts[0] = time()
        elif has_seen_near[0] and time() - ts[0] > 2:
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)
        elif has_seen_near[0] and time() - ts[0] > 3:
            occupied = detector.seat_occupied(frame)
            fsm.pop_state()
            if occupied:
                fsm.push_state(state_find_empty_seat(mega))

    return inner
