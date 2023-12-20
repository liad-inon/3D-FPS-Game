from consts import *
from engine import Engine
from network import *
from ui import UI
from window import Window

class Display:
    """containes the entire graphic display"""
    def __init__(self, game):
        self.game = game
        self.win = Window(RESOLOTION, FPS)
        self.engine = Engine(self)
        self.ui = UI(self)

    def update(self):
        if self.game.network_handler.player_status == IN_MATCH:
            self.engine.draw_frame()
        else:
            self.ui.draw_frame()

        self.win.update()