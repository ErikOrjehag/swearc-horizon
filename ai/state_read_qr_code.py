
import sys, os
sys.path.insert(0, os.path.abspath(".."))
from vision.detect_qr_code import DetectQRCode
import json
from time import time
import pyttsx


def state_read_qr_code(mega):

    qr_detector = DetectQRCode()

    engine = pyttsx.init()
    engine.setProperty("rate", 90)

    def inner(itr, fsm, frame):

        print("read qr code")

        if itr == 0:
            mega.send("lspeed", -10)
            mega.send("rspeed", -10)

        data_str = qr_detector.detect_qr(frame).data

        if data_str:
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)

            data = json.loads(data_str)

            for key, value in data.iteritems():
                value = str(value)
                print(key + ": " + value)
                engine.say(key + ". " + value)

            engine.startLoop(False)
            ts = time()
            while time() - ts < 10:
                engine.iterate()
            engine.stop()

            fsm.pop_state()

    return inner

