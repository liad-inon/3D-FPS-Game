from consts import *
import pygame

class UI:
    def __init__(self, display):
        self.game = display.game

    def draw_frame(self):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render(self.game.network_handler.player_status, True, (255, 255, 255), (0, 0, 0))
        self.game.display.win.screen.blit(text, (0,0))