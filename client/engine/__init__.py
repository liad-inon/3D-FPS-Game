import pygame
import math

from assets import Assets
from engine.bullet_renderer import BulletRenderer
from map import Map
from engine.player_renderer import PlayerRenderer
from utils.pose import Pose
from conf import *
from engine.consts import *


class Engine:
    """Containes the entire in game graphics"""
    def __init__(self, assets:Assets, screen:pygame.Surface, map:Map):
        self.assets = assets
        self.screen = screen
        self.map = map
        
        self.local_player_pose = Pose(0,0,0)# The possion of the player runing on the local computer. Updated by Game.
        self.external_players: dict[str, PlayerRenderer] = {}
        self.bullets: list[BulletRenderer] = []

        self.wall_texture = assets.wall_texture
        self.floor_texture = assets.floor_texture
        self.gun_texture = assets.gun_texture
        self.shoting_animation = assets.shoting_animation

    def update_players(self, external_players_data):

        for player_id in external_players_data.keys():
            if player_id not in self.external_players:
                self.external_players[player_id] = PlayerRenderer(self.assets, self.local_player_pose, external_players_data[player_id])
            else:
                self.external_players[player_id].update_player_data(external_players_data[player_id])

        disconnected_players = set(self.external_players.keys()) - set(external_players_data.keys())
        for player in disconnected_players:
            self.external_players.pop(player)

    def update_bullets(self, bullets_positions):
        self.bullets = [BulletRenderer(self.assets, self.local_player_pose, pos) for pos in bullets_positions]

    def start_shooting_animation(self):
        self.shoting_animation.start()

    def ray_cast(self):
        ray_casting_result = []
        ox, oy = self.local_player_pose.x, self.local_player_pose.y
        x_map, y_map = (int(self.local_player_pose.x), int(self.local_player_pose.y))

        ray_angle = self.local_player_pose.angle - HALF_FOV + 0.0001
        for ray in range(RAYS_NUM):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(RAY_MAX_STEPS):
                tile_hor = int(x_hor), int(y_hor)
                if self.map.collides(tile_hor):
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(RAY_MAX_STEPS):
                tile_vert = int(x_vert), int(y_vert)
                if  self.map.collides(tile_vert):
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth = depth_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth = depth_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.local_player_pose.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            ray_casting_result.append((depth, proj_height, offset))

            ray_angle += DELTA_ANGLE

        return ray_casting_result

    def get_walls_render(self, ray_casting_result):
        """Return the renderd image of the walls"""
        results = []

        for ray, values in enumerate(ray_casting_result):
            depth, proj_height, offset = values

            if proj_height < RESOLOTION[1]:
                wall_column = self.wall_texture.subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * RESOLOTION[1] / proj_height
                wall_column = self.wall_texture.subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, RESOLOTION[1]))
                wall_pos = (ray * SCALE, 0)

            results.append((depth, wall_column, wall_pos))

        return results
    
    def draw_3d_layer(self):
        # Add walls to the draw list
        objects = self.get_walls_render(self.ray_cast())

        # Add players to the draw list
        for id, player in self.external_players.items(): 
            render = player.get_render()
            if render != None:
                objects.append(render)

        # Add bullets to the draw list
        for bullet in self.bullets: 
            render = bullet.get_render()
            if render != None and MIN_BULLET_RENDER_DIST < math.sqrt((bullet.x-self.local_player_pose.x)**2+(bullet.y-self.local_player_pose.y)**2):
                objects.append(render)

        # Draw the draw list by distance from the player
        list_objects = sorted(objects, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            # Adds darknes effect
            image.fill((255/(1+depth**3*0.015), 255/(1+depth**3*0.015), 255/(1+depth**3*0.015), 255), None, pygame.BLEND_RGBA_MULT)
            
            self.screen.blit(image, pos)

    def draw_floor(self):
        self.screen.blit(self.floor_texture, (0,0))

    def draw_gun(self):
        if self.shoting_animation.playing:
            self.shoting_animation.update()
            self.screen.blit(self.shoting_animation.current_frame, (0,GUN_HIGHT))
        else:
            self.screen.blit(self.gun_texture, (0,GUN_HIGHT))

    def draw_winner_losser_banner(self, player_dead, player_won):
        if player_dead:
            self.screen.blit(self.assets.game_over_banner, (0,0))
        elif player_won:
            self.screen.blit(self.assets.victory_banner, (0,0))

    def draw_lives(self, player_lives):
        for heart_num in range(player_lives):
            self.screen.blit(self.assets.heart_icon, (heart_num*108,0))

    def draw_2d_layer(self, player_dead, player_won, player_lives):
        if not player_dead:
            self.draw_gun()
        self.draw_lives(player_lives)
        self.draw_winner_losser_banner(player_dead, player_won)

    def draw_frame(self, player_dead, player_won, player_lives):
        self.screen.fill((0,0,0))
        self.draw_floor()
        self.draw_3d_layer()
        self.draw_2d_layer(player_dead, player_won, player_lives)

        
            
                
