import pickle
import Protocol as p
import graphic as g
import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((p.SERVER_IP, p.SERVER_PORT))


data = pickle.loads(client_socket.recv(p.SOCKET_SIZE))



g.game(data[0], data[1])

client_socket.close()
