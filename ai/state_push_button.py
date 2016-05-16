
from time import time

def state_push_button(mega, nano):

    ts = time()
    has_sent_reverse = [False]

    def inner(itr, fsm, frame):

        if itr == 0:
            mega.send("lspeed", 20)
            mega.send("rspeed", 20)

        time_diff = time() - ts

        if time_diff > 3 and not has_sent_reverse[0]:
            has_sent_reverse[0] = True
            mega.send("lspeed", -20)
            mega.send("rspeed", -20)
        elif time_diff > 5:
            mega.send("lspeed", 0)
            mega.send("rspeed", 0)
            fsm.pop_state()



    return inner
