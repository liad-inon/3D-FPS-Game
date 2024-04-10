import pygame

from utils.animation import Animation
from player import SHOOT_COOLDOWN
from conf import *


class Assets:
        def __init__(self):
                load = lambda x: pygame.image.load(x).convert_alpha()
                
                # Engine
                self.wall_texture = pygame.image.load("textures/wall.png").convert_alpha()
                self.floor_texture = pygame.image.load("textures/floor.png").convert_alpha()

                self.gun_texture = load(f"textures/gun/0.png")
                gun_frames = [load(f"textures/gun/{indx}.png") for indx in range(1, 6)]
                self.shoting_animation = Animation(gun_frames, SHOOT_COOLDOWN / len(gun_frames))
                self.bullet_texture = load("textures/bullet.png")

                self.game_over_banner = load("textures/game-over.png")
                self.victory_banner = load("textures/victory.png")
                self.heart_icon = load("textures/heart.png")

                # Player renderer
                self.player_defult_frame = load("textures/player/MOK1E1.PNG")

                self.standing_animations = {
                'FORWARD': Animation([load("textures/player/MOK1E1.PNG")], 10, True),
                'FORWARD_LEFT': Animation([load("textures/player/MOK1E2.PNG")], 10, True),
                'LEFT': Animation([load("textures/player/MOK1E3.PNG")], 10, True),
                'BACKWARD_LEFT': Animation([load("textures/player/MOK1E4.PNG")], 10, True),
                'BACKWARD': Animation([load("textures/player/MOK1E5.PNG")], 10, True),
                'BACKWARD_RIGHT': Animation([load("textures/player/MOK1E6.PNG")], 10, True),
                'RIGHT': Animation([load("textures/player/MOK1E7.PNG")], 10, True),
                'FORWARD_RIGHT': Animation([load("textures/player/MOK1E8.PNG")], 10, True)
                }

                self.shooting_animations = {
                'FORWARD': Animation([load("textures/player/MOK1G1.PNG")], 10, True),
                'FORWARD_LEFT': Animation([load("textures/player/MOK1G2.PNG")], 10, True),
                'LEFT': Animation([load("textures/player/MOK1G3.PNG")], 10, True),
                'BACKWARD_LEFT': Animation([load("textures/player/MOK1G4.PNG")], 10, True),
                'BACKWARD': Animation([load("textures/player/MOK1G5.PNG")], 10, True),
                'BACKWARD_RIGHT': Animation([load("textures/player/MOK1G6.PNG")], 10, True),
                'RIGHT': Animation([load("textures/player/MOK1G7.PNG")], 10, True),
                'FORWARD_RIGHT': Animation([load("textures/player/MOK1G8.PNG")], 10, True),
                }

                self.walking_animations = {
                'FORWARD': Animation([load(f"textures/player/MOK1{f}1.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'FORWARD_LEFT': Animation([load(f"textures/player/MOK1{f}2.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'LEFT': Animation([load(f"textures/player/MOK1{f}3.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'BACKWARD_LEFT': Animation([load(f"textures/player/MOK1{f}4.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'BACKWARD': Animation([load(f"textures/player/MOK1{f}5.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'BACKWARD_RIGHT': Animation([load(f"textures/player/MOK1{f}6.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'RIGHT': Animation([load(f"textures/player/MOK1{f}7.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                'FORWARD_RIGHT': Animation([load(f"textures/player/MOK1{f}8.PNG") for f in ("A", "B", "C", "D")], WALKIN_ANIMATION_INTERVAL, True),
                }

                self.dying_animation = Animation([load(f"textures/player/MOK1{f}0.PNG") for f in ("I", "J", "K", "L", "M")], DYING_ANIMATION_INTERVAL)

                
                # UI
                self.waiting_for_players_text = load("textures/waiting-for-players.png")
                self.in_queque_text = load("textures/in-queque.png")
                self.not_connected_text = load("textures/not-connected.png")
