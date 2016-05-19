
from time import sleep, time


def state_straighten_up(mega, reverse=0):

    sent_ts = [time()]
    dirr = [0]
    ts = [0]

    def inner(itr, fsm, frame):

        lsonar = mega.get("lsonar")
        rsonar = mega.get("rsonar")

        print("lsonar: " + str(lsonar) + ", rsonar: " + str(rsonar))

        if lsonar and rsonar and not dirr[0]:

            diff = lsonar - rsonar

            print("diff: " + str(diff))

            if abs(diff) < 30:
                fsm.pop_state()
            else:
                ts[0] = time()
                if diff < 0:
                    dirr[0] = 1
                else:
                    dirr[0] = -1

        if dirr[0] and time() - sent_ts[0] > 0.1:
            if time() - ts[0] < 2:
                sent_ts[0] = time()
                mega.send("lspeed", -20)
                mega.send("rspeed", -20)
            if time() - ts[0] < 4:
                sent_ts[0] = time()
                mega.send("lspeed", 20 * -1 * dirr[0])
                mega.send("rspeed", 20 * dirr[0])
            elif time() - ts[0] < 10:
                sent_ts[0] = time()
                mega.send("lspeed", -20)
                mega.send("rspeed", -20)
            else:
                sent_ts[0] = time()
                mega.send("lspeed", 0)
                mega.send("rspeed", 0)
                fsm.pop_state()

    return inner

