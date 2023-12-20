from consts import *
import pygame
import math
import time

class Player:
    def __init__(self, game):
        self.game = game
        self.angle = INIT_ANGLE
        self.pos = INIT_POS
        self.last_shoot_sec = 0
        self.shoot_cooldown = SHOOT_COOLDOWN

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0

        speed = SPEED * self.game.display.win.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        pressed_num = 0

        if keys[pygame.K_w]:
            pressed_num += 1

            dx += speed_cos
            dy += speed_sin

        if keys[pygame.K_a]:
            pressed_num += 1

            dx += speed_sin
            dy -= speed_cos

        if keys[pygame.K_s]:
            pressed_num += 1

            dx -= speed_cos
            dy -= speed_sin

        if keys[pygame.K_d]:
            dx -= speed_sin
            dy += speed_cos

        if pressed_num == 2:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)

        colides_walls = lambda pos: self.game.map.colides(((pos[0]), (pos[1])))

        if not colides_walls((self.pos[0]+dx+(COLISION_BOX_SIZE * (-1 if dx < 0 else 1)), self.pos[1])):
            self.pos[0] += dx
        if not colides_walls((self.pos[0], self.pos[1]+dy+(COLISION_BOX_SIZE * (-1 if dy < 0 else 1)))):
            self.pos[1] += dy

    def rotation(self):
        mx, my = pygame.mouse.get_pos()
        if mx < RESOLOTION[0]/2-MOUSE_BORDER or mx > RESOLOTION[0]/2+MOUSE_BORDER:
            pygame.mouse.set_pos(RESOLOTION[0]/2, RESOLOTION[1]/2)
        
        self.rel = max(min(pygame.mouse.get_rel()[0], MAX_MOUSE_REL), -1*MAX_MOUSE_REL)
        self.angle += self.rel * ROTATION_SPEED * self.game.display.win.delta_time

        if self.angle < 0:
            self.angle += math.pi*2
        elif self.angle > math.pi*2:
            self.angle -= math.pi*2

    def shooting(self):
        if pygame.mouse.get_pressed()[0] and time.time() > (self.last_shoot_sec+self.shoot_cooldown):
            self.last_shoot_sec = time.time()
            self.game.display.engine.start_shooting_animation()

    def update(self):
        self.rotation()
        self.movement()
        self.shooting()


                