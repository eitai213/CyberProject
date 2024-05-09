import socket
import threading
import json
import setting as s  # ייבוא הגדרות
from map import *

# הגדרת כתובת IP מקומית דינמית
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)  # קבלת ה-IP המקומי
print("Server IP:", local_ip)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((local_ip, s.SERVER_PORT))  # שימוש ב-IP המקומי
server_socket.listen(5)  # המספר כאן מציין את מספר החיבורים שהשרת יכול להמתין להם

num_player = 0
data_players = []
treasure = treasure_place()

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

    while True:
        data = conn.recv(s.SOCKET_SIZE)
        if not data:
            break

        received_message = json.loads(data.decode("utf-8"))
        print("Received from client:", received_message)

    conn.close()

while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
