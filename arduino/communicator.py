
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
        if reading:
            return self._parse_reading(reading)
        else:
            return None

    def _parse_reading(self, reading):
        try:
            key, value = reading.split("=")
        except:
            return None

        try:
            if key in ["dsonar"]:
                value = float(value)
            elif key in []:
                value = int(value)
        except:
            print(value)
            return None

        return [key, value]

