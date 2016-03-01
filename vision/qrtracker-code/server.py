import socket
import select
import struct

# who: x, y, phi
# 4B   4B 4B 4B
def encode_message(data):
    name = data[0]
    if len(name)<4:
        for i in range(4-len(name)):
            name+=" "
    elif len(name)>4:
        name = name[:4]
    msg = ""
    for c in name:
        msg += struct.pack("c", c)
    for n in data[1:]:
        msg += struct.pack("f", n)
    return msg

class socket_server:
    def __init__(self, host, port):
        self.backlog = 5
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen(self.backlog)
        self.inputs = [self.s]
        self.outputs = []
        self.in_data = []
        self.out_data = []

    def __del__(self):
        self.s.close()

    def step(self):
        inputready, outputready, exceptready = select.select(self.inputs, [], [], 0)
        for s in inputready:
            if s == self.s:
                client, addr = self.s.accept()
                self.inputs.append(client)
                print "accepted:", client, addr

        if len(self.out_data):
            for msg in self.out_data:
                m = encode_message(msg)
                for s in self.inputs[1:]:
                    s.send(m)
            self.out_data = []

    def push_data(self, data):
        self.out_data.append(data)
