import json
import socket
import game
from setting import *

BROADCAST_PORT = 12344
SERVER_PORT = SERVER_PORT

def discover_server():
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.settimeout(5)

    message = "DISCOVER_SERVER".encode('utf-8')
    broadcast_socket.sendto(message, ('255.255.255.255', BROADCAST_PORT))

    try:
        response_message, server_address = broadcast_socket.recvfrom(1024)
        server_ip = response_message.decode('utf-8')
        print(f"Discovered server at {server_ip}")
        return server_ip
    except socket.timeout:
        print("No response to broadcast, server not found.")
        return None




class Client:
    def __init__(self, name_player="spicy natan", server_ip=discover_server()):
        self.name_player = name_player
        self.server_ip = server_ip

    def run_client(self):
        if self.server_ip:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_ip, SERVER_PORT))

            received_data = client_socket.recv(1024)
            decoded_data = json.loads(received_data.decode("utf-8"))

            print(decoded_data)

            position_player = decoded_data[0][0]
            num_player = decoded_data[0][1]
            treasure_place = decoded_data[1]

            app = game.Game(
                treasure_place=treasure_place,
                position=position_player,
                num_player=num_player,
                client_socket=client_socket,
            )

            app.run()
        else:
            print("Failed to discover server.")


# a = Client("sss")
# a.run_client()