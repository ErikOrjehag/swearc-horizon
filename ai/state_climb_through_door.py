
from time import sleep

def state_climb_trough_door(mega, nano):

    def inner(itr, fsm, frame):
        speed = 20
        elev_pwm = 100

        mega.send("lspeed", speed)
        mega.send("rspeed", speed)
        sleep(6)
        mega.send("lspeed", -speed / 2)
        mega.send("rspeed", -speed / 2)
        sleep(1)
        mega.send("lspeed", 0)
        mega.send("rspeed", 0)

        nano.send("elev", -elev_pwm)
        sleep(4.5)
        nano.send("elev", 0)

        mega.send("lspeed", speed)
        mega.send("rspeed", speed)
        sleep(6)

        mega.send("lspeed", -speed / 2)
        mega.send("rspeed", -speed / 2)
        sleep(0.8)
        mega.send("lspeed", 0)
        mega.send("rspeed", 0)

        nano.send("elev", elev_pwm)
        sleep(16)
        nano.send("elev", 0)

        mega.send("lspeed", speed)
        mega.send("rspeed", speed)
        sleep(4)

        nano.send("elev", elev_pwm)
        sleep(1.5)
        nano.send("elev", -elev_pwm)
        sleep(3)
        mega.send("lspeed", 0)
        mega.send("rspeed", 0)
        sleep(8)
        nano.send("elev", 0)

        fsm.pop_state()

    return inner

