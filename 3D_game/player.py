from setting import *
import pygame as pg
import math

class Player:
    def __init__(self, game, position=PLAYER_POS, num_player=0):
        self.game = game
        self.x, self.y = position
        self.num_player = num_player
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pg.K_SPACE]:
            dz += speed_cos + speed_sin




        self.check_wall_collision(dx, dy)


        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time


        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy


    def check_treasure_collision(self, x, y):
        if self.x >= (x - 0.15) and self.x <= (x + 1) and self.y >= (y - 0.15) and self.y <= (y + 1):
            return False
        else:
            return True


    def draw(self):
  #      pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
 #                    (self.x * 100 + WIDTH * math.cos(self.angle),
#                              self.y * 100 + WIDTH * math.sin(self.angle)),2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    def get_position(self):
        return self.x, self.y

    def get_num_player(self):
        return self.num_player


    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)


