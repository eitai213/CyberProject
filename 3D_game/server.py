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
    for i, player_data in enumerate(data_players):
        if player_data[1] == current_player:
            data_players[i] = new_data
            break

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

SERVER_IP = get_local_ip()
SERVER_PORT = s.SERVER_PORT
BROADCAST_PORT = 12344



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

    print(data_players)

    while True:
        try:
            data = client_socket.recv(s.SOCKET_SIZE)
            if not data:
                print("No data received, closing connection.")
                break


            received_message = json.loads(data.decode("utf-8"))
            update_data_players(received_message[1], received_message)


            json_data = json.dumps(data_players)
            client_socket.sendall(json_data.encode('utf-8'))


            # Print updated player data
            print(data_players)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    client_socket.close()

def broadcast_listener():
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_socket.bind(("", BROADCAST_PORT))

    while True:
        message, address = broadcast_socket.recvfrom(1024)
        print(f"Received broadcast from {address}: {message.decode('utf-8')}")
        if message.decode('utf-8') == "DISCOVER_SERVER":
            response_message = SERVER_IP.encode('utf-8')
            broadcast_socket.sendto(response_message, address)

broadcast_thread = threading.Thread(target=broadcast_listener, daemon=True)
broadcast_thread.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket,)).start()
