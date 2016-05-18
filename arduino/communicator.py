
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
        val = None
        arr = reading.split("=")
        if len(arr) == 2:
            key = arr[0].strip()
            value = arr[1].strip()
            if key in ["dsonar", "lsonar", "rsonar", "fsonar"]:
                try:
                    value = float(value)
                except:
                    # print("warning: " + value)
                    return None
            elif key in ["start"]:
                value = (value == "1")

            val = [key, value]

        return val
