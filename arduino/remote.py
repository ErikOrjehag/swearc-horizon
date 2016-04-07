
from arduino import Arduino
from time import sleep
from random import random
import cv2
import numpy as np


def main():

    arduino = Arduino()
    cv2.imshow("asd", np.zeros((200, 200, 3), dtype=np.uint8))
    keyboard = cv2.waitKey(1)

    while keyboard != ord("q"):
        keyboard = cv2.waitKey(1)

        if keyboard == ord("w"):
            arduino.send("arm", 1)
        elif keyboard == ord("e"):
            arduino.send("arm", 0)
        elif keyboard == ord("r"):
            arduino.send("arm", -1)

        elif keyboard == ord("a"):
            arduino.send("wheel", 1)
        elif keyboard == ord("s"):
            arduino.send("wheel", 0)
        elif keyboard == ord("d"):
            arduino.send("wheel", -1)

if __name__ == "__main__":
    main()
