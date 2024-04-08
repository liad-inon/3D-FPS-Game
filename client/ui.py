import pygame
from assets import Assets
from consts import *


class UI:
    """Containes the entire User Interface"""
    def __init__(self, assets:Assets, screen:pygame.Surface):
        self.assets = assets
        self.screen = screen

    def draw_frame(self, client_status):
        self.screen.fill((0,0,0))
        
        if client_status == WAITING_FOR_PLAYERS:
            self.screen.blit(self.assets.waiting_for_players_text, (0,0))
        elif client_status == IN_QUEQUE:
            self.screen.blit(self.assets.in_queque_text, (0,0))
        elif client_status == NOT_CONNECTED:
            self.screen.blit(self.assets.not_connected_text, (0,0))