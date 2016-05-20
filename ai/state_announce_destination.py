
import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.detect_qr_code import DetectQRCode
import json
from time import time
import pyttsx


def state_announce_destination(destination):

    engine = pyttsx.init()
    engine.setProperty("rate", 90)

    def inner(itr, fsm, frame):

        engine.say("The destination is " + destination[0])

        engine.startLoop(False)
        ts = time()
        while time() - ts < 5:
            engine.iterate()
        engine.stop()

        fsm.pop_state()

    return inner

