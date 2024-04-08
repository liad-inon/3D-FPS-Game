from assets import Assets
from player import Player
from engine.sprite_renderer import SpriteRenderer


class BulletRenderer(SpriteRenderer):
    def __init__(self, assets: Assets, player: Player, pos):

        super().__init__(player, pos, assets.bullet_texture, 0.1, 1.7)
