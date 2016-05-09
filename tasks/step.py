
import sys, os
sys.path.insert(0, os.path.abspath(".."))
from arduino.arduino import Arduino
from time import sleep
from config import mega_usb, nano_usb

def main():

    mega = Arduino(mega_usb)
    nano = Arduino(nano_usb)
    sleep(1)
    # mega.send("light", True)
    speed = 20
    elev_pwm = 70

    mega.send("lspeed", speed)
    mega.send("rspeed", speed)
    sleep(3)
    mega.send("lspeed", 0)
    mega.send("rspeed", 0)

    nano.send("elev", -elev_pwm)
    sleep(10)
    nano.send("elev", 0)

    mega.send("lspeed", speed)
    mega.send("rspeed", speed)
    sleep(5)
    mega.send("lspeed", 0)
    mega.send("rspeed", 0)

    mega.send("lspeed", speed / -2)
    mega.send("rspeed", speed / -2)
    sleep(0.5)
    mega.send("lspeed", 0)
    mega.send("rspeed", 0)

    nano.send("elev", elev_pwm)
    sleep(27)
    nano.send("elev", 0)

    mega.send("lspeed", speed)
    mega.send("rspeed", speed)
    sleep(4)

    nano.send("elev", elev_pwm)
    sleep(1)
    nano.send("elev", -elev_pwm)
    sleep(5)
    mega.send("lspeed", 0)
    mega.send("rspeed", 0)
    mega.send("light", True)
    sleep(10)
    nano.send("elev", 0)
    mega.send("light", False)



if __name__ == "__main__":
    main()
