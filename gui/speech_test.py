import pyttsx
from time import time

engine = pyttsx.init()
engine.say('The quick brown fox jumped over the lazy dog.')
engine.startLoop(False)
ts = time()
while time() - ts < 5:
    print("busy")
    engine.iterate()
engine.stop()
print("done")