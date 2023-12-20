from consts import *
from sprite_renderer import SpriteRenderer
from animation import Animation
import pygame
import math


class AnimationManager:
    """Handle the animation of other players"""

    def __init__(self, player_renderer): 

        self.player_renderer = player_renderer

        self.standing_images = {
            "forward": self.load("textures/player/MOK1E1.PNG"),
            "forward_left": self.load("textures/player/MOK1E2.PNG"),
            "left": self.load("textures/player/MOK1E3.PNG"),
            "backward_left": self.load("textures/player/MOK1E4.PNG"),
            "backward": self.load("textures/player/MOK1E5.PNG"),
            "backward_right": self.load("textures/player/MOK1E6.PNG"),
            "right": self.load("textures/player/MOK1E7.PNG"),
            "forward_right": self.load("textures/player/MOK1E8.PNG")
        }

        self.shooting_images = {
            "forward": self.load("textures/player/MOK1G1.PNG"),
            "forward_left": self.load("textures/player/MOK1G2.PNG"),
            "left": self.load("textures/player/MOK1G3.PNG"),
            "backward_left": self.load("textures/player/MOK1G4.PNG"),
            "backward": self.load("textures/player/MOK1G5.PNG"),
            "backward_right": self.load("textures/player/MOK1G6.PNG"),
            "right": self.load("textures/player/MOK1G7.PNG"),
            "forward_right": self.load("textures/player/MOK1G8.PNG"),
        }

        self.walking_animations = {
            "forward": Animation([self.load(f"textures/player/MOK1{f}1.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "forward_left": Animation([self.load(f"textures/player/MOK1{f}2.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "left": Animation([self.load(f"textures/player/MOK1{f}3.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "backward_left": Animation([self.load(f"textures/player/MOK1{f}4.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "backward": Animation([self.load(f"textures/player/MOK1{f}5.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "backward_right": Animation([self.load(f"textures/player/MOK1{f}6.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "right": Animation([self.load(f"textures/player/MOK1{f}7.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
            "forward_right": Animation([self.load(f"textures/player/MOK1{f}8.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
        }

        self.dying_animation = [self.load(f"textures/player/MOK1{f}0.PNG") for f in ("I", "J", "K", "L", "M")]

        self.last_frame = None
        self.current_animation = self.walking_animations["forward"]
        self.current_animation.start()

    def load(self, path):
        return pygame.image.load(path).convert_alpha()
    
    def get_direction(self):
        """return the direction of the other player from the player's point of view"""
        p1 = self.player_renderer.game_player.pos
        p2 = self.player_renderer.rendered_player_data["pos"]
        p3 = (p2[0]+math.cos(self.player_renderer.rendered_player_data["angle"]), p2[1]+math.sin(self.player_renderer.rendered_player_data["angle"]))
        da = math.degrees(math.atan2(p3[1]-p2[1], p3[0]-p2[0]) - math.atan2(p1[1]-p2[1], p1[0]-p2[0]))
        da = da + 360 if da < 0 else da

        if 22.5 > da or da > 332.5:
            return "forward"
        elif 62.5 > da > 22.5:
            return "forward_left"
        elif 107.5 > da > 62.5:
            return "left"
        elif 152.5 > da > 107.5:
            return "backward_left"
        elif 197.5 > da > 152.5:
            return "backward"
        elif 242.5 > da > 197.5:
            return "backward_right"
        elif 287.5 > da > 242.5:
            return "right"
        elif 332.5 > da > 287.5:
            return "forward_right"
        
        raise ValueError("Angle is not in bound (angle < 0 or angle > 360)")
    
    def update_texture(self):
        """update the texture of the PlayerRenderer"""
        dierection = self.get_direction()
        if self.current_animation is not self.walking_animations[dierection]:
            self.current_animation = self.walking_animations[dierection]
            self.current_animation.start()

        self.current_animation.update()
        self.player_renderer.set_texture(self.current_animation.current_frame)

class PlayerRenderer(SpriteRenderer):
    """Renders other player"""
    def __init__(self, engine, rendered_player_data):
        self.animation_manager = AnimationManager(self)
        super().__init__(engine, rendered_player_data["pos"], self.animation_manager.standing_images["forward"], 0.7, 0.2)
        
        self.engine = engine
        self.game = engine.game
        self.game_player = self.game.player
        self.rendered_player_data = rendered_player_data
        
        self.walking_animation_playing = False
        

    def update_pos(self):
        """Update the other player position"""
        super().x = self.rendered_player_data["pos"][0]
        super().y = self.rendered_player_data["pos"][1]

    def update_player_data(self, data):
        """Update the other player data"""
        self.rendered_player_data = data
        self.update_pos()

    def get_render(self):
        """return the render of the other player"""
        self.animation_manager.update_texture()
        return super().get_render()
        
        