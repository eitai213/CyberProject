import pickle
import socket
import setting as s
import main

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((s.SERVER_IP, s.SERVER_PORT))
server_socket.listen()

num_player = 0
data_players = []

