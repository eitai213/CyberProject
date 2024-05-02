import setting as s
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class Player():
    def __init__(self, position=(0, 0, 0), model='cube'):
        self.position = position
        self.model = model
        self.hp = s.MAX_HP
        self.speed = s.SPEED_PLAYER
        player = FirstPersonController(model=self.model, position=self.position , color=color.orange, origin_y=-.5, speed=self.speed, collider='box')
        player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))


    def update_players(self, players):
        i = 0
        while i < len(players):
            player = Entity(model=players[i].get_model, position=players[i].get_position,
                            origin_y=-.5, speed=s.SPEED_PLAYER, collider='box')
            i += 1


    def get_position(self):
        return self.position

    def change_position(self, position):
        self.position = position

    def get_model(self):
        return self.model

    def change_model(self, model):
        self.model = model
