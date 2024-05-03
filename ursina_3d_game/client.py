from ursina import *
import pickle
import player
import weapon
import socket
import setting as s
import map

app = Ursina()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((s.SERVER_IP, s.SERVER_PORT))

map.Map()
gun = weapon.Gun()


def update():
    gun.update()



data = pickle.loads(client_socket.recv(s.SOCKET_SIZE))
client = player.Player(client=True, num_player=data.get_num_player, position=data.get_position)

app.run()







