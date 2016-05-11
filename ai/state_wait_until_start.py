
def state_wait_until_start(mega):

	def inner(itr, fsm, frame):

		button_pressed = mega.get("button")
		
		if button_pressed:
			fsm.pop_state()
		else:
			print("Waiting...")

	return inner