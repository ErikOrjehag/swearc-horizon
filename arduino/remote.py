
import sys, os
sys.path.insert(0, os.path.abspath(".."))
from arduino.arduino import Arduino
import cv2
import numpy as np
import config


def main():

    lightIsOn = False

    mega = Arduino(config.mega_usb)
    nano = Arduino(config.nano_usb)

    cv2.imshow("asd", np.zeros((200, 200, 3), dtype=np.uint8))

    deg = 90

    keyboard = cv2.waitKey(10) & 0xFF

    while keyboard != ord("q"):
        keyboard = cv2.waitKey(10) & 0xFF
        speed = 30
        if keyboard == ord("w"):
            mega.send("rspeed", speed)
            mega.send("lspeed", speed)
        elif keyboard == ord("s"):
            mega.send("rspeed", -speed)
            mega.send("lspeed", -speed)
        elif keyboard == ord("a"):
            mega.send("rspeed", speed)
            mega.send("lspeed", -speed)
        elif keyboard == ord("d"):
            mega.send("rspeed", -speed)
            mega.send("lspeed", speed)
        elif keyboard == ord("e"):
            mega.send("rspeed", 0)
            mega.send("lspeed", 0)
        elif keyboard == ord("r"):
            lightIsOn = not lightIsOn
            print(lightIsOn)
            mega.send("light", lightIsOn)
        elif keyboard == ord("t"):
            nano.send("elev", 100)
        elif keyboard == ord("y"):
            nano.send("elev", -100)
        elif keyboard == ord("u"):
            nano.send("elev", 0)
        elif keyboard == ord("k"):
            deg = min(deg + 30, 180)
            mega.send("servo", deg)
        elif keyboard == ord("l"):
            deg = max(deg - 30, 0)
            mega.send("servo", deg)
        elif keyboard == ord("j"):
            deg = 90
            mega.send("servo", deg)


if __name__ == "__main__":
    main()
