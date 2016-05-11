import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
import numpy as np
from arduino.arduino import Arduino
from ai.finite_state_machine import FiniteStateMachine
from ai.state_find_button import state_find_button
from ai.state_wait_until_start import state_wait_until_start
from ai.state_move_to_button import state_move_to_button
from ai.state_push_button import state_push_button
from math.kalman import create_default_kalman

cap = cv2.VideoCapture(capture_device)
# cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)

mega = Arduino(mega_usb)
nano = Arduino(nano_usb)

# Wait for camera and usb to settle...
sleep(5)

kalman = create_default_kalman()

fsm = FiniteStateMachine()

fms.push_state(state_celebrate())
fms.push_state(state_read_qr_code())
fsm.push_state(state_push_button(mega, nano))
fsm.push_state(state_move_to_button(kalman, mega, nano, dist_to_btn=300))
fsm.push_state(state_find_button(kalman, mega))
fms.push_state(state_wait_until_start(mega))

while True:
	
	keyboard = cv2.waitKey(1) & 0xFF
	ret, frame = cap.read()

	fsm.update(frame)

	cv2.imshow('frame', frame)

    if keyboard == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()