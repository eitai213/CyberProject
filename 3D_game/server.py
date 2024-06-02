import secure
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
    if ((treasure_position[0] - 0.15) <= player_position[0] <= (treasure_position[0] + 1.15) and
            (treasure_position[1] - 0.15) <= player_position[1] <= (treasure_position[1] + 1.15)):
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
    def __init__(self):
        self.SERVER_IP = get_local_ip()
        self.SERVER_PORT = s.SERVER_PORT
        self.BROADCAST_PORT = s.BROADCAST_PORT
        self.private_key, self.public_key = secure.generate_keys_for_rsa()
        self.num_player = 0
        self.winner = 0
        self.treasure = treasure_place()
        self.treasure_found = 0
        self.data_players = [[self.treasure_found, self.winner]]
        self.start = 0
        self.name_players = []


    def update_data_players(self, current_player, new_data):
        self.data_players[current_player + 1] = new_data

    def update_data_players_after_remove(self, num_player):
        i = num_player
        while i < len(self.data_players):
            self.data_players[i][1] = i
            i += 1

    def get_server_ip(self):
        return self.SERVER_IP

    def replace_keys(self, client_socket):
        try:
            send_public_key = json.dumps(self.public_key.save_pkcs1().decode('utf-8'))
            client_socket.sendall(send_public_key.encode("utf-8"))
            data = client_socket.recv(s.SOCKET_SIZE)
            print(f"Received encrypted AES key: {data}")  # Debugging line
            encrypted_aes_key_hex = json.loads(data.decode("utf-8"))
            encrypted_aes_key = bytes.fromhex(encrypted_aes_key_hex)
            client_aes_key = secure.decrypt_key(self.private_key, encrypted_aes_key)
            print(f"client_aes_key (server){client_aes_key}")
            return client_aes_key
        except Exception as e:
            print(f"Error in replace_keys: {e}")
            raise

    @staticmethod
    def send_message(client_socket, client_aes_key, data):
        try:
            encrypted_data = secure.encrypt_message(client_aes_key, json.dumps(data))
            client_socket.sendall(encrypted_data)
        except Exception as e:
            print(f"Error in send_message: {e}")
            raise

    @staticmethod
    def recv_message(client_socket, client_aes_key):
        try:
            data = client_socket.recv(s.SOCKET_SIZE)
            decode_data = json.loads(secure.decrypt_message(client_aes_key, data))
            print(f"recv data : {decode_data}")
            return decode_data
        except Exception as e:
            print(f"Error in recv_message: {e}")
            raise


    def waiting_room(self, client_socket, server_socket):
        try:
            client_aes_key = self.replace_keys(client_socket)
            while True:
                if self.start == 1:
                    break
            self.handle_client(client_socket, client_aes_key, server_socket)
        except Exception as e:
            print(f"Error in waiting_room: {e}")
            client_socket.close()

    def handle_client(self, client_socket, client_aes_key, server_socket):
        print(f"Connected by {client_socket.getpeername()}")

        new_player = [s.PLAYER_POS, self.num_player]
        self.num_player += 1
        self.data_players.append(new_player)

        try:
            name_player = self.recv_message(client_socket, client_aes_key)
            self.name_players.append(name_player)

            data_to_send = [new_player, self.treasure]
            self.send_message(client_socket, client_aes_key, data_to_send)
            print(f"Initial data sent to client : {data_to_send}")
        except Exception as e:
            print(f"Error sending initial data to client : {e}")
            self.data_players.remove(new_player)
            self.update_data_players_after_remove(new_player[1])
            client_socket.close()
            return

        print(f"Current data players : {self.data_players}")

        while True:
            try:
                data = client_socket.recv(s.SOCKET_SIZE)
                if not data:
                    print("No data received, closing connection.")
                    break

                received_message = json.loads(secure.decrypt_message(client_aes_key, data))
                # print(f"Data received from client : {received_message}")
                self.update_data_players(received_message[1], received_message)
                winner = check_treasure(self.data_players[1:], self.treasure)
                print(winner)
                if winner is not None:
                    self.treasure_found += 1
                    self.data_players[0] = [self.treasure_found, [winner, self.name_players[winner]]]
                    self.send_message(client_socket, client_aes_key, self.data_players)

                    break

                self.send_message(client_socket, client_aes_key, self.data_players)

                print(f"Updated data players: {self.data_players}")

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

        self.data_players.remove(self.data_players[new_player[1] + 1])
        self.num_player -= 1
        self.update_data_players_after_remove(new_player[1])
        client_socket.close()
        server_socket.close()

    def broadcast_listener(self):
        try:
            broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast_socket.bind(("", self.BROADCAST_PORT))

            while True:
                message, address = broadcast_socket.recvfrom(1024)
                print(f"Received broadcast from {address}: {message.decode('utf-8')}")
                if message.decode('utf-8') == "DISCOVER_SERVER":
                    response_message = self.SERVER_IP.encode('utf-8')
                    broadcast_socket.sendto(response_message, address)
        except Exception as e:
            print(f"Error in broadcast_listener: {e}")

    def run_server(self):
        broadcast_thread = threading.Thread(target=self.broadcast_listener, daemon=True)
        broadcast_thread.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.SERVER_IP, self.SERVER_PORT))
        server_socket.listen(5)

        print(f"Server listening on {self.SERVER_IP}:{self.SERVER_PORT}")

        while True:
            try:
                client_socket, addr = server_socket.accept()
                threading.Thread(target=self.waiting_room, args=(client_socket, server_socket)).start()
            except OSError as e:
                print(f"Server socket error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
            if self.treasure_found == 1:
                server_socket.close()
                client_socket.close()
                break



if __name__ == "__main__":
    server = Server()
    server.run_server()
