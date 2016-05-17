
import serial


class Communicator:

    def __init__(self, port):
        """

        :param port: for example "/dev/cu.usbmodem1421"
        """
        self.ser = serial.Serial(port, 9600, timeout=0)

    def write(self, key, value):
        self.ser.write(key + "=" + str(value) + ",")

    def read(self):
        reading = self.ser.readline()
        if reading and "=" in reading:
            return self._parse_reading(reading)
        else:
            # print("warning: " + reading)
            return None

    def _parse_reading(self, reading):
        key, value = reading.split("=")
        key = key.strip()
        value = value.strip()
        if key in ["dsonar"]:
            try:
                value = float(value)
            except:
                print(value)
                value = 0
        elif key in ["start"]:
            value = (value == "1")
        val = [key, value]
        return val