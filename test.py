
import pyttsx
from time import time

engine = pyttsx.init()
engine.setProperty("rate", 90)

engine.say("test test test test test")

engine.startLoop(False)
ts = time()
while time() - ts < 5:
    engine.iterate()
engine.stop()