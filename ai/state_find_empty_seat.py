import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.seat_detector import SeatDetector
import config
from time import time, sleep


def state_find_empty_seat(mega):

    detector = SeatDetector(config.seat_hsv_range)
    has_seen_far = [False]
    has_seen_near = [False]
    ts = [None]
    sent_ts = [time()]

    def inner(itr, fsm, frame):

        #if itr == 0:
        #    mega.send("lspeed", 11)
        #    mega.send("rspeed", 10)

        dist_to_ground = mega.get("dsonar")

        print(dist_to_ground)

        speed = 5

        # line follow
        if time() - sent_ts[0] > 0.5:
            sent_ts[0] = time()
            if dist_to_ground < 25:
                mega.send("rspeed", speed)
                mega.send("lspeed", int(speed * 0.6))
            else:
                mega.send("rspeed", int(speed * 0.6))
                mega.send("lspeed", speed)

        if not has_seen_far[0]:
            distance = mega.get("fsonar")
            print("has not seen far: " + str(distance))
            if distance and distance > 700:
                has_seen_far[0] = True
                t = time()
                while time() - t < 2:
                    mega.update()
                    sleep(0.1)

        elif not has_seen_near[0]:
            distance = mega.get("fsonar")
            print("has not seen near: " + str(distance))
            if distance and 100 < distance < 400:
                has_seen_near[0] = True
                ts[0] = time()
                t = time()
                while time() - t < 2:
                    mega.update()
                    sleep(0.1)

        elif has_seen_near[0] and time() - ts[0] > 5:
            print("look at seat")
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)
            sleep(2)
            occupied = detector.seat_occupied(frame)
            fsm.pop_state()
            if occupied:
                fsm.push_state(state_find_empty_seat(mega))
        else:
            print("chillin")

    return inner
