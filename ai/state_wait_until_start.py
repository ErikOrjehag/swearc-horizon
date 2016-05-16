
from time import time


def state_wait_until_start(mega):
    ts = time()

    def inner(itr, fsm, frame):

        button_pressed = mega.get("button")

        if button_pressed or time() - ts > 5:
            fsm.pop_state()
        else:
            print("Waiting...")

    return inner
