import socket
import threading
import json
import setting as s
from map import treasure_place


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def check_treasure_collision(player_position, treasure_position):
    if (player_position[0] >= (treasure_position[0] - 0.15) and player_position[0] <= (treasure_position[0] + 1.15) and
            player_position[1] >= (treasure_position[1] - 0.15) and player_position[1] <= (treasure_position[1] + 1.15)):
        return True
    else:
        return False


def check_treasure(data_players, treasure_position):
    for player_data in data_players:
        player_position = player_data[0]
        if check_treasure_collision(player_position, treasure_position):
            return player_data[1]
    return None

class Server:
    def __init__(self, host_name="spicy natan"):
        self.host_name = host_name
        self.SERVER_IP = get_local_ip()
        self.SERVER_PORT = s.SERVER_PORT
        self.BROADCAST_PORT = s.BROADCAST_PORT
        self.num_player = 0
        self.data_players = []
        self.treasure = treasure_place()
        self.treasure_found = False

    def update_data_players(self, current_player, new_data):
        for i, player_data in enumerate(self.data_players):
            if player_data[1] == current_player:
                self.data_players[i] = new_data
                break

    def get_server_ip(self):
        return self.SERVER_IP

    def handle_client(self, client_socket):
        print(f"Connected by {client_socket.getpeername()}")

        new_player = [s.PLAYER_POS, self.num_player]
        data_to_send = [new_player, self.treasure]

        json_data = json.dumps(data_to_send)
        client_socket.sendall(json_data.encode("utf-8"))

        self.num_player += 1
        self.data_players.append(new_player)

        print(self.data_players)

        while True:
            try:
                data = client_socket.recv(s.SOCKET_SIZE)
                if not data:
                    print("No data received, closing connection.")
                    break

                received_message = json.loads(data.decode("utf-8"))
                self.update_data_players(received_message[1], received_message)

                winner = check_treasure(self.data_players, self.treasure)
                if winner:
                    self.treasure_found = True
                    json_data = json.dumps([winner, self.treasure_found])
                    self.broadcast_to_all_clients(json_data)
                    break

                else:
                    # Send updated player data to all clients
                    json_data = json.dumps(self.data_players)
                    self.broadcast_to_all_clients(json_data)

                print(self.data_players)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

        client_socket.close()

    def broadcast_to_all_clients(self, message):
        for player_data in self.data_players:
            try:
                client_socket = player_data[2]
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to client: {e}")

    def broadcast_listener(self):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadcast_socket.bind(("", self.BROADCAST_PORT))

        while True:
            message, address = broadcast_socket.recvfrom(1024)
            print(f"Received broadcast from {address}: {message.decode('utf-8')}")
            if message.decode('utf-8') == "DISCOVER_SERVER":
                response_message = self.SERVER_IP.encode('utf-8')
                broadcast_socket.sendto(response_message, address)

    def run_server(self):
        broadcast_thread = threading.Thread(target=self.broadcast_listener, daemon=True)
        broadcast_thread.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.SERVER_IP, self.SERVER_PORT))
        server_socket.listen(5)

        print(f"Server listening on {self.SERVER_IP}:{self.SERVER_PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            self.data_players.append([s.PLAYER_POS, self.num_player, client_socket])
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            if self.treasure_found:
                server_socket.close()
                print("server closed")
                break
