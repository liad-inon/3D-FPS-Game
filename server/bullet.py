import math
from conf import *


class Bullet:
    def __init__(self, pos, angle, shooter_momentum):
        self.pos = pos
        self.angle = angle

        self.momentum_x = math.cos(self.angle) + shooter_momentum[0]
        self.momentum_y = math.sin(self.angle) + shooter_momentum[1] 
        #position the bullet outside of the shooter
        self.pos[0] += self.momentum_x * (PLAYER_RADIUS + 0.01)
        self.pos[1] += self.momentum_y * (PLAYER_RADIUS + 0.01)

    def move(self, runtime_delta):
        speed = BULLET_SPEED * runtime_delta
        self.pos[0] += speed * self.momentum_x
        self.pos[1] += speed * self.momentum_y
        print(self.pos)

    def collides_wall(self, map):
        print(map.collides(self.pos))
        return map.collides(self.pos) or ()
    
    def collides_player(self, player_pos):
        return math.sqrt((player_pos[0]-self.pos[0])**2 + (player_pos[1]-self.pos[1])**2) < PLAYER_RADIUS

