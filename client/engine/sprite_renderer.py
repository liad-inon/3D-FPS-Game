import pygame
import math

from conf import *
from engine.consts import *


class SpriteRenderer:
    """Renders Sprite in 3D space"""
    def __init__(self, player_pose, pos, texture, SPRITE_SCALE, SPRITE_HEIGHT_SHIFT):
        self.player_pose = player_pose

        self.x, self.y = pos
        
        self.set_texture(texture)

        self.sprite_half_width = 0
        self.SPRITE_SCALE = SPRITE_SCALE
        self.SPRITE_HEIGHT_SHIFT = SPRITE_HEIGHT_SHIFT

    def set_texture(self, texture):
        """Sets the texture of the sprite"""
        self.texture = texture

        self.image_width = self.texture.get_width()
        self.image_half_width = self.texture.get_width() // 2
        self.image_ratio = self.image_width / self.texture.get_height()

    def get_projection(self, norm_dist, screen_x):
        """Returns the render of the sprite."""
        proj = SCREEN_DIST / norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.image_ratio, proj

        image = pygame.transform.scale(self.texture, (proj_width, proj_height))

        sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = screen_x - sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        return (norm_dist, image, pos)

    def get_render(self):
        """Check if the sprite is in the screen and return the render"""
        dx = self.x - self.player_pose.x
        dy = self.y - self.player_pose.y
        dx, self.dy = dx, dy
        theta = math.atan2(dy, dx)

        delta = theta - self.player_pose.angle
        if (dx > 0 and self.player_pose.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        dist = math.hypot(dx, dy)
        norm_dist = dist * math.cos(delta)
        if -self.image_half_width < screen_x < (RESOLOTION[0] + self.image_half_width) and norm_dist > 0.5:
            return self.get_projection(norm_dist, screen_x)
        
        