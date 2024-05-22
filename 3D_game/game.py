import json
from setting import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
import pygame as pg
import sys

class Game:
    def __init__(self, treasure_place, screen=pg.display.set_mode(RES), position=PLAYER_POS, num_player=0, client_socket=None):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = screen
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.map = Map(self, treasure_place=treasure_place)
        self.player = Player(self, position=position, num_player=num_player)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.client_socket = client_socket

    def update(self):
        self.player.update()
        self.ray_casting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption("Game")

    def draw(self):
        if self.client_socket:
            data_players = self.get_data_from_server()
            if data_players[-1] == True:
                self.client_socket.close()
                if data_players[0] == self.player.num_player:
                    self.object_renderer.draw_winner_background()
                else:
                    self.object_renderer.draw_losing_background(data_players[0])
                pg.display.update()

            self.map.update_other_player(data_players)
            self.object_renderer.draw()
            self.map.clean_old_position_of_other_player(data_players)
        else:
            self.screen.fill('black')
            self.object_renderer.draw()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()


    def send_to_server(self):
        data = [self.player.get_position(), self.player.num_player]
        json_data = json.dumps(data)
        self.client_socket.sendall(json_data.encode("utf-8"))
        # print(f"Sent data to server: {json_data}")


    def get_data_from_server(self):
        data = self.client_socket.recv(SOCKET_SIZE)
        received_message = json.loads(data.decode("utf-8"))
        return received_message


    def run(self):
        if self.client_socket:
            while True:
                self.check_events()
                self.send_to_server()
                self.update()
                self.draw()
        else:
            while self.player.check_treasure_collision(self.map.x, self.map.y):
                self.check_events()
                self.update()
                self.draw()
            self.object_renderer.draw_winner_background()
            pg.display.update()