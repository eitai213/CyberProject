import socket
import pickle
import setting as s
import main

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((s.SERVER_IP, s.SERVER_PORT))

