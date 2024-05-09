import pickle
import random
import socket
import player
import setting as s

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((s.SERVER_IP, s.SERVER_PORT))
server_socket.listen()

print(f"Server listening on {s.SERVER_IP} : {s.SERVER_PORT}")

num_player = 0
data_players = []

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

new_player = player.Player(num_player=num_player, position=(random.randint(0, 9), 0,random.randint(0, 9)))
data_players.append(new_player)
num_player += 1


client_socket.send(pickle.dumps(new_player))



