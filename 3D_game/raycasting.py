# raycasting.py

from setting import *
import pygame as pg
import math

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.treasure_pos = (self.game.map.x, self.game.map.y)  # מיקום האוצר

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV

        # עבור כל קרן, בצע רייקאסטינג כדי למצוא התנגשות עם קירות
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # לתקן אפסים כדי להימנע מחלוקה באפס
            sin_a = sin_a if sin_a != 0 else 1e-6
            cos_a = cos_a if cos_a != 0 else 1e-6

            # בדיקה התנגשות אופקית
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # בדיקת התנגשות אנכית
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # בחר את הפגיעה הקרובה ביותר
            depth = min(depth_vert, depth_hor)

            # חישוב זווית לתיקון אפקט הדג זהב
            depth *= math.cos(self.game.player.angle - ray_angle)

            # הגובה המוקרן של האובייקט בקירבה למסך
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # צביעת הקיר בהתאם לעומק
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            pg.draw.rect(
                self.game.screen, color,
                (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
            )

            # אם הקרן פגעה באוצר, צייר את האובייקט התלת-ממדי
            treasure_x, treasure_y = self.treasure_pos
            if int(x_vert) == int(treasure_x) and int(y_vert) == int(treasure_y):
                # צייר קובייה שמסמלת את האוצר
                cube_size = proj_height / 6
                pg.draw.rect(
                    self.game.screen, 'yellow',
                    (ray * SCALE, HALF_HEIGHT - cube_size // 2, SCALE, cube_size)
                )

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()

