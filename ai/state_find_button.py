import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
import numpy as np
from vision.button_detector import ButtonDetector
import config


def state_find_button(kalman, mega): 

    button_detector = ButtonDetector(config.btn_hsv_range)

	def inner(itr, fsm, frame):
		
		if itr == 0:
			mega.send("rspeed", 10)
			mega.send("lspeed", 10)

		ellipse = button_detector.find_button(frame)

		if ellipse:
			mega.send("rspeed", 0)
			mega.send("lspeed", 0)
			fsm.pop_state()

	return inner