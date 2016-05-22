import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.seat_detector import SeatDetector
import config
from time import time, sleep


def state_find_empty_seat2(mega):

    detector = SeatDetector(config.seat_hsv_range)
    sent_ts = [time()]
    edge_distance = 50
    occupied_time = 8
    has_seen_near = [False]
    ts = [0]

    def inner(itr, fsm, frame):

        dist_to_ground = mega.get("dsonar")

        print(str(mega.get("rsonar")))
        print(has_seen_near[0])
        #return


        speed = 5

        # line follow
        if time() - sent_ts[0] > 0.2:
            sent_ts[0] = time()
            if dist_to_ground > edge_distance:
                mega.send("rspeed", speed - 3)
                mega.send("lspeed", speed)
            else:
                mega.send("rspeed", speed)
                mega.send("lspeed", speed - 1)

        if 10 < mega.get("rsonar") < 200:
            has_seen_near[0] = True

        occupied = detector.seat_occupied(frame)

        if not occupied and has_seen_near[0]:
            if not ts[0]:
                ts[0] = time()
            elif time() - ts[0] > occupied_time:
                mega.send("rspeed", 0)
                mega.send("lspeed", 0)
                fsm.pop_state()

    return inner

