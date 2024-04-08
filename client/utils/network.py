import socket
import select
import time
import dataclasses
import pickle


@dataclasses.dataclass
class Packet:
    data: dict
    type: str
    time = None

    def sign_time(self):
        self.time = time.time()


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

        def dataclass_from_dict(klass, d):
            try:
                fieldtypes = {f.name:f.type for f in dataclasses.fields(klass)}
                return klass(**{f:dataclass_from_dict(fieldtypes[f],d[f]) for f in d})
            except:
                return d # not a dataclass field
        
        ready = select.select([self.socket], [], [], 0)

        if ready[0]:
            message_header = self.socket.recv(self.message_header_size)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())

            return dataclass_from_dict(Packet, pickle.loads(self.socket.recv(message_length)[self.message_header_size+1:]))

        return False

    def send_packet(self, packet: Packet):
        packet.sign_time()
        packet = pickle.dumps(dataclasses.asdict(packet))
        message_header = f"{len(packet):<{self.message_header_size}}".encode('utf-8')
        self.socket.send(message_header + packet)