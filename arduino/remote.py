
from arduino import Arduino
from time import sleep
from random import random
import cv2
import numpy as np


def main():

    lightIsOn = False

    mega = Arduino("/dev/cu.wchusbserial14110")
    nano = Arduino("/dev/cu.wchusbserial1420")

    cv2.imshow("asd", np.zeros((200, 200, 3), dtype=np.uint8))
    
    keyboard = cv2.waitKey(10) & 0xFF

    while keyboard != ord("q"):
        keyboard = cv2.waitKey(10) & 0xFF

        if keyboard == ord("w"):
            mega.send("rspeed", 20)
            mega.send("lspeed", 20)
        elif keyboard == ord("s"):
            mega.send("rspeed", -20)
            mega.send("lspeed", -20)
        elif keyboard == ord("a"):
            mega.send("rspeed", 20)
            mega.send("lspeed", -20)
        elif keyboard == ord("d"):
            mega.send("rspeed", -20)
            mega.send("lspeed", 20)
        elif keyboard == ord("e"):
            mega.send("rspeed", 0)
            mega.send("lspeed", 0)
        elif keyboard == ord("r"):
            lightIsOn = not lightIsOn
            print(lightIsOn)
            mega.send("light", lightIsOn)
        elif keyboard == ord("t"):
            nano.send("elev", 70)
        elif keyboard == ord("y"):
            nano.send("elev", -70)
        elif keyboard == ord("u"):
            nano.send("elev", 0)

if __name__ == "__main__":
    main()
