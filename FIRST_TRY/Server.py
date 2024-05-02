import socket
import pickle
from Player import Player
from Protocol import SERVER_IP, SERVER_PORT, SOCKET_SIZE

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

data_players = []
player_num = 0

client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")
new_player = Player()
new_player.random_position()
new_player.set_player_num(player_num)
data_players.append(new_player)
client_socket.send(pickle.dumps([new_player, data_players]))
player_num += 1






client_socket.close()
print(f"Connection with {client_address} closed")
