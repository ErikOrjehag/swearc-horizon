import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
from arduino.arduino import Arduino
from ai.finite_state_machine import FiniteStateMachine
from ai.state_find_button import state_find_button
from ai.state_wait_until_start import state_wait_until_start
from ai.state_move_to_button import state_move_to_button
from ai.state_move_to_button2 import state_move_to_button2
from ai.state_celebrate import state_celebrate
from ai.state_find_door import state_find_door
from ai.state_climb_through_door import state_climb_trough_door
from ai.state_straighten_up import state_straighten_up
from ai.state_find_button2 import state_find_button2
from ai.state_find_button_turn import state_find_button_turn
from calc.kalman import create_default_kalman
import config
from time import sleep, time

cap = cv2.VideoCapture(config.capture_device)

mega = Arduino(config.mega_usb)
nano = Arduino(config.nano_usb)
sleep(2)
mega.send("servo", 180)
sleep(1)
mega.send("servo", 180)

kalman = create_default_kalman()

fsm = FiniteStateMachine()

fsm.push_state(state_celebrate(mega))
fsm.push_state(state_climb_trough_door(mega, nano))

# OBS
fsm.push_state(state_find_button_turn(kalman, mega))

# rak
#fsm.push_state(state_move_to_button2(kalman, mega, nano, dist_to_btn=400))

# sne
fsm.push_state(state_find_button2(kalman, mega))

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