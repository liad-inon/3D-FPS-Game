import pickle
from re import T
import socket
import select
import time
from typing import Any, Callable


class Packet(object):
    def __init__(self, data, type):
        self.type = type
        self.data = data
        self.creation_time = time.time()


class Server:
    def __init__(self, host, port, message_header_size, on_connect: Callable[[socket], Any], on_disconnect: Callable[[socket], Any]):
        self.message_header_size = message_header_size
        self.host = host
        self.port = port
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.socket]

        self.start()

    def start(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def handle_clients(self):
        """
            Recive new packets and handle connects and disconnects.
        """
        packets_recived = {}

        read_sockets, _, exception_sockets = select.select(
            self.sockets_list, [], self.sockets_list, 0)

        # Iterate over notified sockets
        for notified_socket in read_sockets:

            if notified_socket == self.socket:
                self.connect_client()

            else:
                packet = self.receive_packet(notified_socket)

                if packet is False:
                    self.disconnect_client(notified_socket)

                    continue

                packets_recived[notified_socket] = packet

        for notified_socket in exception_sockets:
            self.disconnect_client(notified_socket)

        return packets_recived

    def connect_client(self):
        client_socket, client_address = self.socket.accept()

        self.sockets_list.append(client_socket)
        self.on_connect(client_socket)

    def disconnect_client(self, client_socket):
        try:
            self.sockets_list.remove(client_socket)
        except Exception as p: print(p)
        self.on_disconnect(client_socket)

    def send_packet(self, client_socket, packet: Packet):
        packet = pickle.dumps(packet)
        message_header = f"{len(packet):<{self.message_header_size}}".encode(
            'utf-8')
        
        try:
            client_socket.send(message_header + packet)
        except:
            self.disconnect_client(client_socket)

    def receive_packet(self, client_socket):
        try:
            message_header = client_socket.recv(self.message_header_size)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())

            packet = pickle.loads(client_socket.recv(message_length)[
                                  self.message_header_size+1:])

            return packet

        except:
            return False

    def get_client_list(self):
        # return the socket list with out the server socket which is the first element
        return self.sockets_list[1:]