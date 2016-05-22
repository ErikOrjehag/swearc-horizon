
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

        qr = qr_detector.detect_qr(frame)

        if qr:
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)

            data = json.loads(qr.data)

            unix = int(data["time"])
            mins = int((unix - time()) / 60)
            hours = int(mins // 60)
            mins -= int(hours * 60)

            engine.say("Your seat number is " + str(data["seat"]) + " and your train leaves in " + str(hours) + " hours and " + str(mins) + " minutes.")

            engine.startLoop(False)
            ts = time()
            while time() - ts < 20:
                engine.iterate()
            engine.stop()

            fsm.pop_state()

    return inner

