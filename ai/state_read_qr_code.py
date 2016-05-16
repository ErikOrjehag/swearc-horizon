
import sys, os
sys.path.insert(0, os.path.abspath(".."))

from vision.detect_qr_code import DetectQRCode


def state_read_qr_code(mega):

    qr_detector = DetectQRCode()

    def inner(itr, fsm, frame):

        print("read qr code")

        if itr == 0:
            mega.send("lspeed", -10)
            mega.send("rspeed", -10)

        data = qr_detector.detect_qr(frame)

        if data:
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)
            print(data)
            fsm.pop_state()

    return inner
