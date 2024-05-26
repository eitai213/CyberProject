import socket
import threading
import json
import time

import setting as s
from map import treasure_place

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def check_treasure_collision(player_position, treasure_position):
    if (player_position[0] >= (treasure_position[0] - 0.15) and player_position[0] <= (treasure_position[0] + 1.15) and
            player_position[1] >= (treasure_position[1] - 0.15) and player_position[1] <= (treasure_position[1] + 1.15)):
        return False
    else:
        return True

def check_treasure(data_players, treasure_position):
    i = 0
    while i < len(data_players):
        if not check_treasure_collision(data_players[i][0], treasure_position):
            return data_players[i][1]
        i += 1
    return None

class Server:
    def __init__(self, host_name="spicy natan"):
        self.host_name = host_name
        self.SERVER_IP = get_local_ip()
        self.SERVER_PORT = s.SERVER_PORT
        self.BROADCAST_PORT = s.BROADCAST_PORT
        self.num_player = 0
        self.winner = 0
        self.treasure = treasure_place()
        self.treasure_found = 0
        self.data_players = [[self.treasure_found, self.winner]]
        self.start = 0
        self.name_players = []

    def update_data_players(self, current_player, new_data):
        self.data_players[current_player + 1] = new_data

    def get_server_ip(self):
        return self.SERVER_IP

    def waiting_room(self, client_socket, server_socket):
        data = client_socket.recv(s.SOCKET_SIZE)
        received_message = json.loads(data.decode("utf-8"))
        self.name_players.append(received_message)

        while True:
            if self.start == 1:
                json_data = json.dumps(self.name_players)
                client_socket.sendall(json_data.encode("utf-8"))
                break
        self.handle_client(client_socket, server_socket)


    def handle_client(self, client_socket, server_socket):
        print(f"Connected by {client_socket.getpeername()}")

        new_player = [s.PLAYER_POS, self.num_player]
        self.num_player += 1
        self.data_players.append(new_player)

        try:
            data_to_send = [new_player, self.treasure]
            json_data = json.dumps(data_to_send)
            client_socket.sendall(json_data.encode("utf-8"))
            print(f"Initial data sent to client: {data_to_send}")
        except Exception as e:
            print(f"Error sending initial data to client: {e}")
            self.data_players.remove(new_player)
            client_socket.close()
            return

        print(f"Current data players: {self.data_players}")

        while True:
            try:
                data = client_socket.recv(s.SOCKET_SIZE)
                if not data:
                    client_socket.close()
                    server_socket.close()
                    print("No data received, closing connection.")
                    break

                received_message = json.loads(data.decode("utf-8"))
                print(f"Data received from client: {received_message}")
                self.update_data_players(received_message[1], received_message)
                winner = check_treasure(self.data_players[1:], self.treasure)
                print(winner)
                if winner != None:
                    self.treasure_found += 1
                    self.data_players[0] = [self.treasure_found, winner]
                    json_data = json.dumps(self.data_players)
                    client_socket.sendall(json_data.encode("utf-8"))
                    if self.treasure_found > 1:
                        break
                else:
                    json_data = json.dumps(self.data_players)
                    client_socket.sendall(json_data.encode("utf-8"))

                print(f"Updated data players: {self.data_players}")

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

        self.data_players.remove(self.data_players[new_player[1] + 1])
        client_socket.close()


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
            threading.Thread(target=self.waiting_room, args=(client_socket, server_socket)).start()
            if self.treasure_found:
                server_socket.close()
                print("Server closed")
                break

if __name__ == "__main__":
    server = Server()
    server.run_server()
