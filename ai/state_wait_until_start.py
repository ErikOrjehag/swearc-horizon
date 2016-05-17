
from time import time


def state_wait_until_start(mega):
    ts = time()

    def inner(itr, fsm, frame):

        if itr == 0:
            mega.send("start", True)

        button_pressed = mega.get("start")

        if button_pressed:
            mega.send("start", False)
            fsm.pop_state()
        else:
            print("Waiting...")

    return inner
