
from communicator import Communicator
from config import serial_port


class Arduino:

    def __init__(self):
        self.com = Communicator(serial_port)
        self.values = dict()

    def send(self, key, value):
        self.com.write(key, value)

    def get(self, key):
        if key in self.values:
            return self.values[key]
        else:
            return None

    def update(self):
        reading = self.com.read()
        while reading:
            self.values[reading[0]] = reading[1]
            reading = self.com.read()
