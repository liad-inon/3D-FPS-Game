import random
import threading
import math
from network import *
from conf import *
from bullet import Bullet
from map import Map

# server status
WAITING_FOR_PLAYERS = 'WAITING_FOR_PLAYERS'
IN_MATCH = 'IN_MATCH'
#client status
IN_QUEQUE = 'IN_QUEQUE'


class GameServer:
    def __init__(self):
        self.server = Server("127.0.0.1", 1234, 10, self.on_connect, self.on_disconnect)
        
        self.game_status = WAITING_FOR_PLAYERS
        self.map = Map()
        self.players = []
        self.players_in_match = []
        self.players_in_quque = []
        self.players_data = {}
        self.bullets = []

        self.delta_time_calc_time = time.time()
        self.last_game_update = 0

    def on_connect(self, player):
        print("Player connected: " + str(player))
        self.players.append(player)
        self.players_in_quque.append(player)
        self.server.send_packet(player, Packet({'STATUS': WAITING_FOR_PLAYERS if self.game_status == WAITING_FOR_PLAYERS else IN_QUEQUE}, 'STATUS'))

    def on_disconnect(self, player):
        try_to_remove = lambda data, x: data.remove(x) if x in data else None

        try_to_remove(self.players_in_match, player)
        try_to_remove(self.players, player)
        try_to_remove(self.players_in_quque, player)
        self.players_data.pop(hash(player)) if hash(player) in self.players_data.keys() else None

        if len(self.players_in_match) < 2:
            self.game_status = WAITING_FOR_PLAYERS
            
            for player in self.players:
                self.server.send_packet(player, Packet({'STATUS': WAITING_FOR_PLAYERS}, 'STATUS'))

    def init_map_and_players(self):
        map_size = (len(self.players_in_match)*MAP_SIZE_TO_PLAYERS_RATIO+1, len(self.players_in_match)*MAP_SIZE_TO_PLAYERS_RATIO+1)
        self.map.generate_map(map_size)
        spawning_spaces = list(filter(lambda item: item not in self.map.colision_map, [(raw, cloumn) for cloumn in range(map_size[1]) for raw in range(map_size[0])]))

        while True:
            for player in self.players_in_match:
                pos = random.choice(spawning_spaces)
                self.players_data[hash(player)] = {"pos": [pos[0]+0.5, pos[1]+0.5], "angle": self.map.opening_angle(pos), "lives": PLAYER_LIVES, "last_walking_time": 0, "last_shooting_time": 0}

            if False not in [(player1 == player2 or self.map.separated_by_wall(self.players_data[player1]["pos"], self.players_data[player2]["pos"])) for 
                                    player1 in self.players_data.keys() for player2 in self.players_data.keys()]:
                break

    def start_new_match(self):
        self.game_status = IN_MATCH
        self.players_in_match += self.players_in_quque
        self.players_in_quque = []
        self.players_data = {}

        self.init_map_and_players()

        for player in self.players_in_match:
            self.server.send_packet(player, Packet({'MAP_ARRAY': self.map.map_array} , 'INIT_MAP'))
            self.server.send_packet(player, Packet({'POS': self.players_data[hash(player)]["pos"], 
                                                    'ANGLE': self.players_data[hash(player)]["angle"], 
                                                    'LIVES': self.players_data[hash(player)]["lives"]}, 'INIT_PLAYER'))
            self.server.send_packet(player, Packet({'STATUS': IN_MATCH}, 'STATUS'))

    def end_match(self):
        self.game_status = WAITING_FOR_PLAYERS

    def check_win_condition(self):
        alive_players = list(filter(lambda player: self.players_data[hash(player)]["lives"] > 0, self.players_in_match))

        if len(alive_players) <= 1:
            self.server.send_packet(alive_players[0], Packet({}, 'WIN'))

            timer = threading.Timer(8, self.end_match)
            timer.start()
            
    def tick_bullets(self):
        delta_time = time.time()-self.delta_time_calc_time
        self.delta_time_calc_time = time.time()
        
        for bullet in self.bullets:
            bullet.move(delta_time)

            if bullet.collides_wall(self.map):
                self.bullets.remove(bullet)
            else:
                for player in self.players_in_match:
                    if bullet.collides_player(self.players_data[hash(player)]["pos"]):
                        self.players_data[hash(player)]["lives"] -= 1
                        self.server.send_packet(player, Packet({}, 'BULLET_HIT'))
                        self.check_win_condition()

                        self.bullets.remove(bullet) if bullet in self.bullets else None

    def update_players_on_game(self):
        """ Sends the players the required data to render other players """
        for player in self.players_in_match:
            other_players_data = {k: v for k, v in self.players_data.items() if k != hash(player)}
            self.server.send_packet(player, Packet({'DATA': other_players_data}, 'EXTERNAL_PLAYERS_DATA'))

            self.server.send_packet(player, Packet({'POSITIONS': [bullet.pos for bullet in self.bullets]}, 'BULLETS_POSITIONS'))

    def update(self):
        if self.last_game_update+GAME_UPDATE_INTERVAL < time.time():
            self.last_game_update = time.time()

            if self.game_status == WAITING_FOR_PLAYERS and len(self.players) >= 2:
                self.start_new_match()
            elif self.game_status == IN_MATCH:
                self.tick_bullets()
                self.update_players_on_game()

        packets = self.server.handle_clients()
        
        for client, packet in packets.items():
            if self.players_data[hash(client)]["lives"] > 0:
                if packet.type == "player_pos":
                    self.players_data[hash(client)]["pos"] = packet.data
                    self.players_data[hash(client)]["last_walking_time"] = time.time()
                    
                elif packet.type == "player_angle":
                    self.players_data[hash(client)]["angle"] = packet.data

                elif packet.type == "player_shoot":
                    print("shoot")
                    self.bullets.append(Bullet(self.players_data[hash(client)]["pos"][:], self.players_data[hash(client)]["angle"], packet.data))
                    self.players_data[hash(client)]["last_shooting_time"] = time.time()

                

if __name__ == "__main__":
    game_server = GameServer()
    while True:
        game_server.update()