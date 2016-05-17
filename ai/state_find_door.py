
from time import sleep


def state_find_door(mega):

    def inner(itr, fsm, frame):

        print("hello")

        mega.send("lspeed", 15)
        mega.send("rspeed", -15)

        print("hola")

        sleep(8)

        mega.send("lspeed", 15)
        mega.send("rspeed", 15)

        sleep(7)

        mega.send("lspeed", -15)
        mega.send("rspeed", 15)

        sleep(8.5)

        mega.send("lspeed", 0)
        mega.send("rspeed", 0)

        fsm.pop_state()

    return inner

