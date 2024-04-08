import pygame
import math
import time

from utils.event_stack import EventStack
from conf import *


EVENT_MOVEMENT = 'MOVEMENT'
EVENT_ROTATION = 'ROTATION'
EVENT_SHOOTING = 'SHOOTING'


class Player:
    def __init__(self, map):
        self.map = map

        self.raised_events = EventStack()

        self.dead = False
        self.angle = None
        self.pos = None
        self.lives = None

        self.last_shoot_sec = 0
        self.last_pos = None
        self.last_angle = None
        self.current_momentum = [0, 0]

    def init(self, pos, angle, lives):
        """For initialization from server data"""
        self.pos = pos
        self.angle = angle
        self.lives = lives

        self.dead = False

    def remove_life(self):
        self.lives -= 1

        if self.lives < 1:
            self.dead = True
        
    def movement(self, delta_time):
        """Handles player movement"""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        momentum_x, momentum_y = 0, 0

        speed_sin = SPEED * sin_a
        speed_cos = SPEED * cos_a

        keys = pygame.key.get_pressed()
        pressed_num = 0

        if keys[pygame.K_w]:
            pressed_num += 1

            momentum_x += speed_cos
            momentum_y += speed_sin

        if keys[pygame.K_a]:
            pressed_num += 1

            momentum_x += speed_sin
            momentum_y -= speed_cos

        if keys[pygame.K_s]:
            pressed_num += 1

            momentum_x -= speed_cos
            momentum_y -= speed_sin

        if keys[pygame.K_d]:
            momentum_x -= speed_sin
            momentum_y += speed_cos

        if pressed_num == 2:
            momentum_x *= 1 / math.sqrt(2)
            momentum_y *= 1 / math.sqrt(2)

        colides_walls = lambda pos: self.map.collides(((pos[0]), (pos[1])))

        if not colides_walls((self.pos[0]+momentum_x+(COLISION_BOX_SIZE * (-1 if momentum_x < 0 else 1)), self.pos[1])):
            self.pos[0] += momentum_x * delta_time
            self.current_momentum[0] = momentum_x
        if not colides_walls((self.pos[0], self.pos[1]+momentum_y+(COLISION_BOX_SIZE * (-1 if momentum_y < 0 else 1)))):
            self.pos[1] += momentum_y  * delta_time
            self.current_momentum[1] = momentum_y

        if self.last_pos != self.pos:
            self.raised_events.push(EVENT_MOVEMENT)
            self.last_pos = self.pos[:]
            

    def rotation(self, delta_time):
        """Handles player mouse rotation"""
        mx, my = pygame.mouse.get_pos()
        if mx < RESOLOTION[0]/2-MOUSE_BORDER or mx > RESOLOTION[0]/2+MOUSE_BORDER:
            pygame.mouse.set_pos(RESOLOTION[0]/2, RESOLOTION[1]/2)
        
        self.rel = max(min(pygame.mouse.get_rel()[0], MAX_MOUSE_REL), -1*MAX_MOUSE_REL)
        self.angle += self.rel * ROTATION_SPEED * delta_time

        if self.angle < 0:
            self.angle += math.pi*2
        elif self.angle > math.pi*2:
            self.angle -= math.pi*2

        if self.last_angle != self.angle:
            self.raised_events.push(EVENT_ROTATION)
            self.last_angle = self.angle

    def shooting(self):
        """Handles player gun"""
        if pygame.mouse.get_pressed()[0] and time.time() > (self.last_shoot_sec+SHOOT_COOLDOWN):
            self.last_shoot_sec = time.time()
            self.raised_events.push(EVENT_SHOOTING)

    def update(self, delta_time):
        self.rotation(delta_time)
        self.movement(delta_time)
        self.shooting()


                