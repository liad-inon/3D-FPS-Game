from network import *

class GameServer:
    def __init__(self):
        self.server = Server("127.0.0.1", 1234, 10, self.on_connect, self.on_disconnect)
        
        self.game_status = "waiting for players"
        self.players = []
        self.players_in_match = []
        self.players_in_quque = []
        self.players_data = {}
        self.bullets_pos = {}

    def on_connect(self, player):
        print("Player connected: " + str(player))
        self.players.append(player)
        self.players_in_quque.append(player)
        self.server.send_packet(player, Packet("waiting for players" if self.game_status == "waiting for players" else "in quque", "player_status"))

    def on_disconnect(self, player):
        try_to_remove = lambda data, x: data.remove(x) if x in data else None

        try_to_remove(self.players_in_match, player)
        try_to_remove(self.players, player)
        try_to_remove(self.players_in_quque, player)
        try_to_remove(self.players_data, player)
        try_to_remove(self.bullets_pos, player)

        if len(self.players_in_match) < 2:
            self.game_status = "waiting for players"
            
            for player in self.players:
                self.server.send_packet(player, Packet("waiting for players", "player_status"))

    def spawn_players(self):
        for player in self.players_in_match:
            self.players_data[hash(player)] = {"pos": (2, 2), "angle": 0, "walking": False, "dead": False}

    def start_new_game(self):
        self.game_status = "in match"
        self.players_in_match += self.players_in_quque
        self.players_data = {}

        self.spawn_players()

        for player in self.players_in_match:
            self.server.send_packet(player, Packet("in match", "player_status"))

            other_players_data = {k: v for k, v in self.players_data.items() if k != hash(player)}
            self.server.send_packet(player, Packet(other_players_data, "players_data"))

    def update(self):
        packets = self.server.handle_clients()

        if self.game_status == "waiting for players" and len(self.server.get_client_list()) >= 2:
            self.start_new_game()
        
        '''for packet in packets:
            if packet.type == "player_pos":
                pass'''
                


if __name__ == "__main__":
    game_server = GameServer()
    while True:
        game_server.update()