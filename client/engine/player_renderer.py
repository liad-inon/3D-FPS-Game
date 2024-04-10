import time
import math

from assets import Assets
from utils.pose import Pose
from engine.sprite_renderer import SpriteRenderer
from conf import *


class AnimationManager:
    """Handle the animation of PlayerRenderer"""

    def __init__(self, player_renderer, local_player_pose, assets): 

        self.player_renderer = player_renderer
        self.local_player_pose = local_player_pose

        self.defult_frame = assets.player_defult_frame
        self.standing_animations = assets.standing_animations
        self.shooting_animations = assets.shooting_animations
        self.walking_animations = assets.walking_animations
        self.dying_animation = assets.dying_animation
        
        self.last_frame = None
        self.current_animation = self.walking_animations['FORWARD']
        self.current_animation.start()
    
    def direction(self):
        """return the direction of the rendered player from the game player point of view"""
        p1 = (self.local_player_pose.x, self.local_player_pose.y)
        p2 = self.player_renderer.player_data['POS']
        p3 = (p2[0]+math.cos(self.player_renderer.player_data['ANGLE']), p2[1]+math.sin(self.player_renderer.player_data['ANGLE']))
        da = math.degrees(math.atan2(p3[1]-p2[1], p3[0]-p2[0]) - math.atan2(p1[1]-p2[1], p1[0]-p2[0]))
        da = da + 360 if da < 0 else da

        if 22.5 > da or da > 332.5:
            return 'FORWARD'
        elif 62.5 > da > 22.5:
            return 'FORWARD_LEFT'
        elif 107.5 > da > 62.5:
            return 'LEFT'
        elif 152.5 > da > 107.5:
            return 'BACKWARD_LEFT'
        elif 197.5 > da > 152.5:
            return 'BACKWARD'
        elif 242.5 > da > 197.5:
            return 'BACKWARD_RIGHT'
        elif 287.5 > da > 242.5:
            return 'RIGHT'
        elif 332.5 > da > 287.5:
            return 'FORWARD_RIGHT'
        
        raise ValueError("Angle is not in bound (angle < 0 or angle > 360)")
    
    def update_frame(self):
        """update the texture of the PlayerRenderer"""
        dierection = self.direction()
        player_data = self.player_renderer.player_data

        if player_data['LIVES'] <= 0:
            if self.current_animation is not self.dying_animation:
                self.current_animation = self.dying_animation
                self.current_animation.start()

        elif player_data['LAST_SHOOTING_TIME']+OTHER_PLAYERS_SHOOT_DUR > time.time():
            if self.current_animation is not self.shooting_animations[dierection]:
                self.current_animation = self.shooting_animations[dierection]
                self.current_animation.start()

        elif player_data['LAST_WALKING_TIME']+OTHER_PLAYERS_WALK_TIMEOUT > time.time():
            if self.current_animation is not self.walking_animations[dierection]:
                self.current_animation = self.walking_animations[dierection]
                self.current_animation.start()
            
        elif self.current_animation is not self.standing_animations[dierection]:
            self.current_animation = self.standing_animations[dierection]
            self.current_animation.start()

        self.current_animation.update()
        self.player_renderer.set_texture(self.current_animation.current_frame)


class PlayerRenderer(SpriteRenderer):
    """Renders external player"""
    def __init__(self, assets: Assets, local_player_pose: Pose, player_data):
        self.animation_manager = AnimationManager(self, local_player_pose, assets)
        super().__init__(local_player_pose, player_data['POS'], self.animation_manager.defult_frame, 0.7, 0.3)
        
        self.player_data = player_data

    def update_player_data(self, data):
        self.player_data = data
        self.x = self.player_data['POS'][0]
        self.y = self.player_data['POS'][1]

    def get_render(self):
        self.animation_manager.update_frame()
        return super().get_render()
        
        