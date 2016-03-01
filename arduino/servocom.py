
from arduino import Arduino
from time import sleep
from random import random
import cv2
import numpy as np


def main():

    arduino = Arduino()
    cv2.imshow("asd", np.zeros((200, 200, 3), dtype=np.uint8))
    keyboard = cv2.waitKey(1)
    deg = 90
    step = 20

    while keyboard != ord('q'):
        keyboard = cv2.waitKey(1)

        if keyboard == 63235:
            deg = min(180, deg + step)
        elif keyboard == 63234:
            deg = max(0, deg - step)

        arduino.update()
        value = arduino.get("test")

        if value:
            print("value is: " + str(value))

        arduino.send("servo", deg)
        print("sent", deg)

        sleep(.01)

if __name__ == "__main__":
    main()