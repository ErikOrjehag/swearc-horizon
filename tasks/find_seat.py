import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
from arduino.arduino import Arduino
from ai.finite_state_machine import FiniteStateMachine
from ai.state_find_button import state_find_button
from ai.state_wait_until_start import state_wait_until_start
from ai.state_move_to_button import state_move_to_button
from ai.state_push_button import state_push_button
from ai.state_read_qr_code import state_read_qr_code
from ai.state_celebrate import state_celebrate
from ai.state_find_empty_seat import state_find_empty_seat
from calc.kalman import create_default_kalman
import config
from time import sleep

cap = cv2.VideoCapture(config.capture_device)

mega = Arduino(config.mega_usb)
nano = Arduino(config.nano_usb)
sleep(1)

kalman = create_default_kalman()

fsm = FiniteStateMachine()

fsm.push_state(state_celebrate(mega))
fsm.push_state(state_find_empty_seat(mega))
fsm.push_state(state_wait_until_start(mega))

mega.send("servo", 0)

while True:

    keyboard = cv2.waitKey(1) & 0xFF
    ret, frame = cap.read()

    mega.update()
    nano.update()
    fsm.update(frame)

    height, width = frame.shape[:2]
    cv2.line(frame, (int(width / 2), 0), (int(width / 2), height), (255, 255, 255), 1)
    cv2.line(frame, (0, int(height / 2)), (width, int(height / 2)), (255, 255, 255), 1)
    cv2.circle(frame, (int(width / 2), int(height / 2)), int(height * 0.2), (255, 255, 255), 1)

    cv2.imshow('frame', frame)

    if keyboard == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()