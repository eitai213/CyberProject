import socket
import threading
import json
import setting as s  # ייבוא הגדרות
from map import *

num_player = 0
data_players = []
treasure = treasure_place()


def update_data_players(current_player, new_data):
    global data_players
    i = 0
    while i < len(data_players):
        if i == current_player:
            data_players[i] = new_data
            break
        i += 1


# הגדרת כתובת IP מקומית דינמית
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)  # קבלת ה-IP המקומי
print("Server IP:", local_ip)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((local_ip, s.SERVER_PORT))  # שימוש ב-IP המקומי
server_socket.listen(5)  # המספר כאן מציין את מספר החיבורים שהשרת יכול להמתין להם


print("Waiting for connections...")


# פונקציה לטיפול בכל לקוח בנפרד
def handle_client(conn, addr):
    global num_player
    global data_players
    global treasure

    print(f"Connected by {addr}")

    new_player = [s.PLAYER_POS, num_player]
    data_to_send = [new_player, treasure]

    json_data = json.dumps(data_to_send)
    conn.sendall(json_data.encode("utf-8"))

    num_player += 1
    data_players.append(new_player)

    while True:
        data = conn.recv(s.SOCKET_SIZE)
        if not data:
            break

        received_message = json.loads(data.decode("utf-8"))

        #print("Received from client:", received_message)

        update_data_players(received_message[1], received_message)

        print(data_players)

    conn.close()


while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
