
from time import sleep, time


def state_straighten_up(mega, reverse=0):

    reversing = [False]
    ts = [time()]

    def inner(itr, fsm, frame):

        lsonar = mega.get("lsonar")
        rsonar = mega.get("rsonar")

        print("lsonar: " + str(lsonar) + ", rsonar: " + str(rsonar))

        if lsonar and rsonar:

            diff = lsonar - rsonar

            print("diff: " + str(diff))

            if abs(diff) < 20 or reversing[0]:
                if not reversing[0]:
                    print("back up!!!!!!")
                    mega.send("lspeed", -15)
                    mega.send("rspeed", -15)
                    reversing[0] = True
                    ts[0] = time()
                elif time() - ts[0] > reverse:
                    mega.send("lspeed", 0)
                    mega.send("rspeed", 0)
                    fsm.pop_state()
                else:
                    print("backasdasd")
            else:
                if diff > 0:
                    mega.send("lspeed", 3)
                    mega.send("rspeed", -3)
                else:
                    mega.send("lspeed", 3)
                    mega.send("rspeed", -3)

    return inner

