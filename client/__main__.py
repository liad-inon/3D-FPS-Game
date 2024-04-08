from assets import Assets
from engine import Engine
from map import Map
from utils.network import Client, Packet
import player
from ui import UI
from utils.window import Window
from consts import *
from conf import *

class Game:
    """Contain the entire game logic"""

    def __init__(self):
        self.client = Client("127.0.0.1", 1234, 10)
        self.win = Window(RESOLOTION, FPS)
        self.assets = Assets()
        self.map = Map()
        self.player = player.Player(self.map)
        self.engine = Engine(self.assets, self.win.screen, self.map)
        self.ui = UI(self.assets, self.win.screen)

        self.client_status = NOT_CONNECTED
        self.player_won = False

    def initialize(self):
        self.client.connect()

    def tick(self):
        packets = self.client.recive()

        for packet in packets:
            if packet.type == 'STATUS':
                self.client_status = packet.data['STATUS']

            elif packet.type == 'INIT_MAP':
                self.map.init(packet.data['MAP_ARRAY'])

            elif packet.type == 'INIT_PLAYER':
                self.player.init(packet.data['POS'], packet.data['ANGLE'], packet.data['LIVES'])
                
                self.engine.local_player_pose.set_pos(packet.data['POS'])
                self.engine.local_player_pose.angle = packet.data['ANGLE']

                self.player_won = False

            elif packet.type == 'EXTERNAL_PLAYERS_DATA':
                self.engine.update_players(packet.data['DATA'])
            
            elif packet.type == 'BULLETS_POSITIONS':
                self.engine.update_bullets(packet.data['POSITIONS'])

            elif packet.type == 'BULLET_HIT':
                self.player.remove_life()

            elif packet.type == 'WIN':
                self.player_won = True

        if self.client_status == IN_MATCH:
            self.player.update(self.win.delta_time)

            for event in self.player.raised_events:
                if event == player.EVENT_MOVEMENT:
                    self.engine.local_player_pose.set_pos(self.player.pos)
                    self.client.send_packet(Packet((self.player.pos), "player_pos"))
                    
                elif event ==  player.EVENT_ROTATION:
                    self.engine.local_player_pose.angle = self.player.angle
                    self.client.send_packet(Packet(self.player.angle, "player_angle"))

                elif event == player.EVENT_SHOOTING:
                    self.engine.start_shooting_animation()
                    self.client.send_packet(Packet(self.player.current_momentum, "player_shoot"))

            self.engine.draw_frame(self.player.dead, self.player_won, self.player.lives)
        else:
            self.ui.draw_frame(self.client_status)

        self.win.update()

    def run(self):
        self.initialize()
        
        while True:
            self.tick()

if __name__ == '__main__':
    Game().run()