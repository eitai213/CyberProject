import setting as s
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class Player:
    def __init__(self, client=False, num_player=0, position=(0, 0, 0), model='cube'):
        self.num_player = num_player
        self.position = position
        self.model = model
        self.hp = s.MAX_HP
        self.speed = s.SPEED_PLAYER
        if client:
            player = FirstPersonController(model=self.model, position=self.position, color=color.orange, origin_y=-.5, speed=self.speed, collider='box')
            player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))





    def update_players(self, data_players):
        i = 0
        while i < len(data_players):
            player = Entity(model=data_players[i].get_model, position=data_players[i].get_position,
                            origin_y=-.5, speed=s.SPEED_PLAYER, collider='box')
            i += 1


    def get_num_player(self):
        return self.num_player

    def get_position(self):
        return self.position[0], self.position[1], self.position[2]

    def change_position(self, position):
        self.position = position

    def get_model(self):
        return self.model

    def change_model(self, model):
        self.model = model

