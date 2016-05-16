
from time import time


def state_celebrate(mega):

    ts = [0]

    def inner(itr, fsm, frame):

        print("celebrate")

        if itr == 0:
            ts[0] = time()
            mega.send("light", True)

        elif time() - ts > 5:
            mega.send("light", False)
            exit(0)

    return inner
