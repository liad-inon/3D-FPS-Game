from consts import *
import pygame
import math

class SpriteRenderer:
    def __init__(self, engine, pos, texture, SPRITE_SCALE, SPRITE_HEIGHT_SHIFT):
        self.engine = engine
        self.game = engine.game
        self.player = self.game.player

        self.x, self.y = pos
        
        self.set_texture(texture)

        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = SPRITE_SCALE
        self.SPRITE_HEIGHT_SHIFT = SPRITE_HEIGHT_SHIFT

    def set_texture(self, texture):
        self.texture = texture

        self.IMAGE_WIDTH = self.texture.get_width()
        self.IMAGE_HALF_WIDTH = self.texture.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.texture.get_height()

    def get_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pygame.transform.scale(self.texture, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        return (self.norm_dist, image, pos)

    def get_render(self):
        dx = self.x - self.player.pos[0]
        dy = self.y - self.player.pos[1]
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (RESOLOTION[0] + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            return self.get_projection()
        
        