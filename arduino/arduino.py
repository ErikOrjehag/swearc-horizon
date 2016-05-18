
from communicator import Communicator


class Arduino:

    def __init__(self, serial_port):
        self.com = Communicator(serial_port)
        self.values = dict()
        self.values_hist = dict()

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

            if reading[0] not in self.values_hist:
                self.values_hist[reading[0]] = []
            self.values_hist[reading[0]].append(reading[1])
            if len(self.values_hist[reading[0]]) > 5:
                self.values_hist[reading[0]].pop(0)

            self.values[reading[0]] = reading[1]
            reading = self.com.read()

        for id in ["dsonar", "lsonar", "rsonar", "fsonar"]:
            if id in self.values_hist:
                cpy = self.values_hist[id][:]
                cpy.sort()
                self.values[id] = cpy[len(cpy) // 2]

        #if "fsonar" in self.values_hist:
        #    print(self.values_hist["fsonar"])
