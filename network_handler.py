from consts import *
from network import *
from player_renderer import PlayerRenderer


class NetworkHandler:
    def __init__(self, game):
        self.game = game
        self.client = Client("127.0.0.1", 1234, 10)
        
        self.connected = False
        self.player_status = NOT_CONNECTED

        self.last_player_pos = None

    def connect(self):
        try:
            self.client.connect()
            self.connected = True
        except Exception as e:
            print(e)

    def handle_messages(self):
        try:
            packets = self.client.recive()
        except:
            self.player_status = COMUNIOCATION_LOST
            return

        for packet in packets:
            if packet.type == "player_status":
                self.player_status = packet.data
            if packet.type == "players_data":
                self.other_players_pos = packet.data
                self.game.display.engine.other_players = dict((player, PlayerRenderer(self.game.display.engine, data)) for player, data in packet.data.items())
                self.game.other_players = packet.data.items()

    def update_server(self):
        if self.game.player.pos != self.last_player_pos:
            self.client.send_packet(Packet(self.game.player.pos), "player_pos")

    def handle(self):
        if self.connected == False:
            self.connect()
        else:
            self.handle_messages()
