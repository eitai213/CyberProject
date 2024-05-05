from setting import *
from map import *
from player import *
from raycasting import *
from sprite_object import *
import pygame as pg
import sys



class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self)


    def update(self):
        self.player.update()
        self.raycasting.update()
        self.static_sprite.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption("Game")

    def draw(self):
        self.screen.fill('black')
        #self.map.draw()
        #self.player.draw()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.type == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while (self.player.check_treasure_collision(self.map.x, self.map.y)):
            self.check_events()
            self.update()
            self.draw()
        print("you win!!!!")



app = Game()
app.run()
