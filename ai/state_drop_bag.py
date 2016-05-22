
from time import sleep


def state_drop_bag(mega, nano):

    def inner(itr, fsm, frame):
        speed = 20
        elev_pwm = 255

        forward_time = 7
        lift_time = 9 * 6
        back_time = 4

        mega.send("lspeed", speed)
        mega.send("rspeed", speed)
        sleep(forward_time)
        mega.send("lspeed", 0)
        mega.send("rspeed", 0)

        nano.send("elev", -elev_pwm)
        sleep(lift_time)
        nano.send("elev", 0)

        mega.send("lspeed", -speed)
        mega.send("rspeed", -speed)
        sleep(back_time)
        mega.send("lspeed", 0)
        mega.send("rspeed", 0)

        fsm.pop_state()

    return inner


