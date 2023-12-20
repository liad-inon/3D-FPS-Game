from consts import *
from animation import *
from player_renderer import PlayerRenderer
import pygame
import math

class Engine:
    def __init__(self, display):
        self.game = display.game
        self.screen = display.win.screen

        self.wall_texture = pygame.image.load("textures/wall.png").convert_alpha()
        self.floor_texture = pygame.image.load("textures/floor.png").convert_alpha()

        self.cell_px_size = 1
        self.other_players: dict[str, PlayerRenderer] = {}

        self.gun_texture = pygame.image.load(f"textures/gun/0.png")
        gun_frames = [pygame.image.load(f"textures/gun/{indx}.png") for indx in range(1, 6)]
        self.shoting_animation = Animation(gun_frames, self.game.player.shoot_cooldown / len(gun_frames))

    def start_shooting_animation(self):
        self.shoting_animation.start()

    def get_ray_cast(self):
        ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = (int(self.game.player.pos[0]), int(self.game.player.pos[1]))

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
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
                if self.game.map.colides(tile_hor):
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
                if  self.game.map.colides(tile_vert):
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
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            ray_casting_result.append((depth, proj_height, offset))

            ray_angle += DELTA_ANGLE

        return ray_casting_result

    def get_walls_render(self, ray_casting_result):
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
        objects = self.get_walls_render(self.get_ray_cast())
        for id, player in self.other_players.items(): 
            render = player.get_render()
            if render != None:
                objects.append(render)

        list_objects = sorted(objects, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            #add darknes
            image.fill((255/(1+depth**3*0.015), 255/(1+depth**3*0.015), 255/(1+depth**3*0.015), 255), None, pygame.BLEND_RGBA_MULT)
            
            self.screen.blit(image, pos)

    def draw_floor(self):
        self.screen.blit(self.floor_texture, (0,0))

    def draw_gun(self):
        if self.shoting_animation.playing:
            self.shoting_animation.update()
            self.screen.blit(self.shoting_animation.current_frame, (0,0))
        else:
            self.screen.blit(self.gun_texture, (0,0))

    def draw_2d_layer(self):
        self.draw_gun()

    def draw_frame(self):
        self.screen.fill((0,0,0))
        self.draw_floor()
        self.draw_3d_layer()
        self.draw_gun()

        
            
                
