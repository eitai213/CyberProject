import pygame
import pygame as pg
from setting import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('assets/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.losing_image = self.get_texture('assets/losing_background.png', RES)
        self.winner_image = self.get_texture('assets/winner_background.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_winner_background(self):
        self.screen.blit(self.winner_image, (0, 0))

    def draw_losing_background(self, name_player):
        self.screen.blit(self.losing_image, (0, 0))
        large_text = pygame.font.Font(None, 40)
        text_surf, text_rect = text_objects(str(name_player), large_text)
        text_rect.center = (HALF_WIDTH, HALF_HEIGHT + 100)
        self.screen.blit(text_surf, text_rect)


    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = self.game.ray_casting.objects_to_render
        for depth, image, pos in sorted(list_objects, key=lambda x: x[0], reverse=True):
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('assets/1.png'),
            2: self.get_texture('assets/treasure.png'),
            3: self.get_texture('assets/3.png'),
        }
    