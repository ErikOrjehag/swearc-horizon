
import serial
from time import time

ser = serial.Serial("/dev/cu.usbmodem1421", 9600)

maximum = 670
minimum = 300

counter = 0
startTime = time()

while True:

	counter += 1
	if time() - startTime > 1:
		print "ups: " + str(counter)
		counter = 0
		startTime = time()

	
	reading = ser.readline()

	try:

		reading = float(reading.split("=")[1])
	except:
		continue
	
	result = reading - minimum
	result = result / (maximum - minimum)
	result *= 255
	result = max(0, min(255, result))
	result = int(result)
	result = 255 - result

	command = "brightness=" + str(result)

	#print command

	ser.write(command)