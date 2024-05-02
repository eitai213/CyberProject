import random


class Player:
    def __init__(self):
        self.player_num = 0
        self.position = [0, 0, 0]
        self.rotation_angle = 0

    def __str__(self):
        return """
        player_num : {player_num} 
        position : {position}
        rotation_angle : {rotation_angle}
        """.format(player_num=self.player_num, position=self.position, rotation_angle=self.rotation_angle)



    def get_player_num(self):
        return self.player_num

    def get_position(self):
        return self.position

    def get_rotation_angle(self):
        return self.rotation_angle

    def set_player_num(self,num):
        self.player_num = num

    def set_position(self, position):
        self.position = position

    def set_rotation_angle(self, rotation_angle):
        self.rotation_angle = rotation_angle




    def random_position(self):
        self.position = [random.randint(0, 10), 0, random.randint(0, 10)]
        return self.position




