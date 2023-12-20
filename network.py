from consts import *
import pickle 
import socket
import select
import time


class Packet(object):
    def __init__(self, data, type):
        self.type = type
        self.data = data
        self.creation_time = time.time()

class Client:
    def __init__(self, ip, port, message_header_size):
        self.ip = ip
        self.port = port
        self.message_header_size = message_header_size

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.socket.setblocking(False)

    def recive(self):
        recived = []

        while True:
            packet = self.receive_packet()

            if packet is False:
                return recived

            recived.append(packet)

    def receive_packet(self):
        ready = select.select([self.socket], [], [], 0)

        if ready[0]:
            message_header = self.socket.recv(self.message_header_size)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())

            return pickle.loads(self.socket.recv(message_length)[self.message_header_size+1:])

        return False

    def send_packet(self, packet: Packet):
        packet = pickle.dumps(packet)
        message_header = f"{len(packet):<{self.message_header_size}}".encode(
            'utf-8')
        self.socket.send(message_header + packet)