
import sys, os
sys.path.insert(0, os.path.abspath(".."))
from arduino.arduino import Arduino
from time import sleep
from config import mega_usb, nano_usb

def main():

    mega = Arduino(mega_usb)
    sleep(1)

    while True:
        mega.update()
        distance = mega.get("dsonar")

        if distance < 200:
            mega.send("rspeed", 7)
            mega.send("lspeed", 5)
        else:
            mega.send("rspeed", -5)
            mega.send("lspeed", 7)

        print(distance)

        sleep(0.05)

if __name__ == "__main__":
    main()
