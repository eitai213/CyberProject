import socket
import threading
import json
import setting as s
from map import treasure_place

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


def get_local_ip():
    """פונקציה שמחזירה את כתובת ה-IP הפנימית של המחשב"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


# הגדרות השרת
SERVER_IP = get_local_ip()
SERVER_PORT = s.SERVER_PORT
BROADCAST_PORT = 12344  # פורט להאזנה להודעות broadcast


def handle_client(client_socket):
    global num_player
    global data_players
    global treasure

    print(f"Connected by {client_socket.getpeername()}")

    new_player = [s.PLAYER_POS, num_player]
    data_to_send = [new_player, treasure]

    json_data = json.dumps(data_to_send)
    client_socket.sendall(json_data.encode("utf-8"))

    num_player += 1
    data_players.append(new_player)

    while True:
        data = client_socket.recv(s.SOCKET_SIZE)
        if not data:
            break

        received_message = json.loads(data.decode("utf-8"))
        update_data_players(received_message[1], received_message)
        print(data_players)

    client_socket.close()


def broadcast_listener():
    """מאזין להודעות broadcast ושולח חזרה את כתובת ה-IP של השרת"""
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_socket.bind(("", BROADCAST_PORT))

    while True:
        message, address = broadcast_socket.recvfrom(1024)
        print(f"Received broadcast from {address}: {message.decode('utf-8')}")
        if message.decode('utf-8') == "DISCOVER_SERVER":
            response_message = SERVER_IP.encode('utf-8')
            broadcast_socket.sendto(response_message, address)


# יצירת סוקט של השרת
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

# יצירת תהליך נפרד להאזנה להודעות broadcast
broadcast_thread = threading.Thread(target=broadcast_listener, daemon=True)
broadcast_thread.start()

while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket,)).start()
