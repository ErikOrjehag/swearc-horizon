
from arduino import Arduino
from time import sleep
from random import random
import cv2
import numpy as np


def main():

    lightIsOn = False

    arduino = Arduino("/dev/ttyUSB0")
    cv2.imshow("asd", np.zeros((200, 200, 3), dtype=np.uint8))
    keyboard = cv2.waitKey(10) & 0xFF

    while keyboard != ord("q"):
        keyboard = cv2.waitKey(10) & 0xFF

        if keyboard == ord("w"):
            arduino.send("rspeed", 20)
            arduino.send("lspeed", 20)
        elif keyboard == ord("s"):
            arduino.send("rspeed", -20)
            arduino.send("lspeed", -20)
        elif keyboard == ord("a"):
            arduino.send("rspeed", 20)
            arduino.send("lspeed", -20)
        elif keyboard == ord("d"):
            arduino.send("rspeed", -20)
            arduino.send("lspeed", 20)
        elif keyboard == ord("e"):
            arduino.send("rspeed", 0)
            arduino.send("lspeed", 0)
        elif keyboard == ord("r"):
            lightIsOn = not lightIsOn
            print(lightIsOn)
            arduino.send("light", lightIsOn)

if __name__ == "__main__":
    main()
