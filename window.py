from consts import *
import pygame;
import sys;

class Window:
    def __init__(self, size, fps):
        self.screen = pygame.display.set_mode(size)
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.delta_time = 0

    def update(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        self.check_exit()

    def check_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()


    