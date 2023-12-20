from consts import *
from map import *
from player import *
from window import *
from engine import *
from player_renderer import *
from network_handler import *
from ui import *
from display import *
import pygame

pygame.font.init()

class Game:
    def __init__(self):
        self.map = Map(self, MAP_SIZE[0], MAP_SIZE[1])
        self.player = Player(self)
        self.display = Display(self)
        self.network_handler = NetworkHandler(self)

        self.other_players_pos = {}

    def update(self):
        self.network_handler.handle()
        self.display.update()
        self.player.update()

    def run(self):
        while True:
            self.update()

if __name__ == '__main__':
    Game().run()