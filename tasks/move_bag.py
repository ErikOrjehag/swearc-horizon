import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
from arduino.arduino import Arduino
from ai.finite_state_machine import FiniteStateMachine
from ai.state_find_button import state_find_button
from ai.state_wait_until_start import state_wait_until_start
from ai.state_move_to_button import state_move_to_button
from ai.state_push_button import state_push_button
from ai.state_celebrate import state_celebrate
from ai.state_move_to_bag import state_move_to_bag
from ai.state_announce_destination import state_announce_destination
from ai.state_lift_bag import state_lift_bag
from ai.state_find_destination import state_find_destination
from ai.state_move_to_human import state_move_to_human
from ai.state_greet_human import state_greet_human
from ai.state_find_destination2 import state_find_destination2
from calc.kalman import create_default_kalman
import config
from time import sleep
from ai.state_drop_bag import state_drop_bag

cap = cv2.VideoCapture(config.capture_device)

mega = Arduino(config.mega_usb)
nano = Arduino(config.nano_usb)
sleep(2)
mega.send("servo", 180)
sleep(1)
mega.send("servo", 80)

destination = [None]
#destination = ["W"]

kalman = create_default_kalman()
kalman2 = create_default_kalman()

fsm = FiniteStateMachine()

fsm.push_state(state_celebrate(mega))
fsm.push_state(state_drop_bag(mega, nano))
fsm.push_state(state_find_destination2(mega, kalman, destination))
fsm.push_state(state_lift_bag(mega, nano))
fsm.push_state(state_announce_destination(destination))
fsm.push_state(state_move_to_bag(mega, kalman, destination, bag_distance=500))
fsm.push_state(state_move_to_human(mega, kalman2))
fsm.push_state(state_wait_until_start(mega))

while True:

    keyboard = cv2.waitKey(1) & 0xFF

    ret, frame = cap.read()

    mega.update()
    nano.update()
    fsm.update(frame)

    cv2.imshow('frame', frame)

    if keyboard == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()