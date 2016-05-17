
from time import time


def state_push_button(mega, nano):

    ts = [0]

    def inner(itr, fsm, frame):

        if itr == 0:
            ts[0] = time()
            mega.send("lspeed", 10)
            mega.send("rspeed", 10)

        time_diff = time() - ts[0]

        if 3 < time_diff:
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)
            fsm.pop_state()

    return inner
