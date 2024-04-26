import socket
from var import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = SERVER_HOST
        self.port = SERVER_PORT
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(BUFFER_SIZE).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(BUFFER_SIZE).decode()
            print('Received: ' + reply)
            return reply
        except socket.error as e:
            return str(e)
