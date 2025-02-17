import random
import pygame as pg

_ = False

mini_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 1],
            [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]




def treasure_place():
    y_max = len(mini_map) - 1
    x_max = len(mini_map[0]) - 1
    while True:
        y = random.randint(0, y_max)
        x = random.randint(0, x_max)
        if mini_map[y][x] != 1:
            return x, y




class Map:
    def __init__(self, game, treasure_place=treasure_place()):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        self.x, self.y = treasure_place
        self.world_map[(self.x, self.y)] = 2

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        for pos in self.world_map:
            if self.world_map[pos] == 1:
                pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)

        for pos, value in self.world_map.items():
            if value == 2:
                pg.draw.circle(self.game.screen, 'red', (pos[0] * 100 + 50, pos[1] * 100 + 50), 30)


    def clean_old_position_of_other_player(self, data_players):
        all_other_players_pos = []
        for player_data in data_players:
            if player_data[-1] != self.game.player.num_player:
                pos = (int(player_data[0][0]), int(player_data[0][1]))
                all_other_players_pos.append(pos)

        for pos in list(self.world_map.keys()):
            if self.world_map[pos] == 3 and pos not in all_other_players_pos:
                del self.world_map[pos]

    def update_other_player(self, data_players):
        for player_data in data_players:
            if player_data[-1] != self.game.player.num_player:
                pos = (int(player_data[0][0]), int(player_data[0][1]))
                self.world_map[pos] = 3
