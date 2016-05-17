
from time import time


def state_wait_until_start(mega):
    ts = time()

    def inner(itr, fsm, frame):

        button_pressed = mega.get("start")

        #print(button_pressed)

        if button_pressed:
            fsm.pop_state()
        else:
            print("Waiting...")

    return inner
