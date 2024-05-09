import json
import socket
from setting import *
from map import *


treasure_place = treasure_place()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

num_player = 0
data_players = []

print("Waiting for a connection...")
conn, addr = server_socket.accept()

new_player = [PLAYER_POS, num_player]
new_client_data = [new_player, treasure_place]

num_player += 1
data_players.append(new_player)

with conn:
    print('Connected by', addr)
    # רשימה לשליחה
    data_to_send = new_client_data

    # המרת הרשימה ל-JSON
    json_data = json.dumps(data_to_send)

    # שליחת הנתונים ללקוח
    conn.sendall(json_data.encode('utf-8'))

    while True:
        data = conn.recv(1024)
        received_message = json.loads(data.decode('utf-8'))
        print(received_message)



