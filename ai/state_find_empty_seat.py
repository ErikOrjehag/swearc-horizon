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
    #has_seen_edge = [False]

    far_distance = 400
    near_distance = 350

    near_distance_r = 200

    chill_time = 3
    edge_distance = 50
    safety_time = 2
    occupied_time = 4

    def inner(itr, fsm, frame):

        dist_to_ground = mega.get("dsonar")

        #print("dist_to_ground: " + str(dist_to_ground))
        #print("fsonar: " + str(mega.get("fsonar")))
        print(str(mega.get("rsonar")))
        #return


        speed = 5

        # line follow
        if time() - sent_ts[0] > 0.5:
            sent_ts[0] = time()
            if dist_to_ground > edge_distance:
                #has_seen_edge[0] = True
                mega.send("rspeed", speed - 3)
                mega.send("lspeed", speed)
            else:
                mega.send("rspeed", speed)
                mega.send("lspeed", speed - 1)

        if not has_seen_far[0]:
            distance = mega.get("fsonar")
            print("has not seen far: " + str(distance))
            if distance and distance > far_distance:
                has_seen_far[0] = True
                t = time()
                while time() - t < safety_time:
                    mega.update()
                    sleep(0.1)

        elif not has_seen_near[0]:
            distance = mega.get("fsonar")
            print("has not seen near: " + str(distance))
            if (distance and 100 < distance < near_distance) or (20 < mega.get("rsonar") < near_distance_r):
                has_seen_near[0] = True
                ts[0] = time()
                t = time()
                while time() - t < safety_time:
                    mega.update()
                    sleep(0.1)

        elif has_seen_near[0] and time() - ts[0] > chill_time:
            print("look at seat")
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)
            sleep(1)
            occupied = detector.seat_occupied(frame)
            fsm.pop_state()
            if occupied:
                fsm.push_state(state_find_empty_seat(mega))
            else:
                sleep(occupied_time)
        else:
            print("chillin")

    return inner

