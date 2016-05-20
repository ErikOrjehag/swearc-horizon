
from time import time
import pyttsx


def state_greet_human(mega):

    engine = pyttsx.init()
    engine.setProperty("rate", 90)

    def inner(itr, fsm, frame):

        print("greet human")

        mega.send("light", True)

        engine.say("Hello human")

        engine.startLoop(False)
        ts = time()
        while time() - ts < 5:
            engine.iterate()
        engine.stop()

        mega.send("light", False)

        fsm.pop_state()

    return inner
