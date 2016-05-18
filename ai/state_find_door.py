
from time import sleep, time

def state_find_door(mega):

    def inner(itr, fsm, frame):

        mega.send("servo", 180)

        print("hello")

        mega.send("lspeed", 15)
        mega.send("rspeed", -15)

        print("hola")

        sleep(8.5)

        mega.send("lspeed", 15)
        mega.send("rspeed", 15)
        sleep(6)

        #ts = time()

        #mega.update()
        #while mega.get("fsonar") > 400 or time() - ts < 2:
        #    mega.update()
        #    print("...")
        #    sleep(0.2)

        #mega.send("lspeed", -15)
        #mega.send("rspeed", -15)

        #sleep((time() - ts) / 2.)

        mega.send("lspeed", -15)
        mega.send("rspeed", 15)

        sleep(8)

        mega.send("lspeed", 0)
        mega.send("rspeed", 0)

        mega.send("servo", 90)

        fsm.pop_state()

    return inner

