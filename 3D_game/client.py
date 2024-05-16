import json
import socket
import game
from setting import *

BROADCAST_PORT = 12344  # אותו פורט כמו בקוד השרת
SERVER_PORT = SERVER_PORT


def discover_server():
    """שולח הודעת broadcast ומחכה לתשובה מהשרת"""
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.settimeout(5)

    message = "DISCOVER_SERVER".encode('utf-8')
    broadcast_socket.sendto(message, ('<broadcast>', BROADCAST_PORT))

    try:
        response_message, server_address = broadcast_socket.recvfrom(1024)
        server_ip = response_message.decode('utf-8')
        print(f"Discovered server at {server_ip}")
        return server_ip
    except socket.timeout:
        print("No response to broadcast, server not found.")
        return None


# גילוי השרת
server_ip = discover_server()
if server_ip:
    # יצירת סוקט של הלקוח
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, SERVER_PORT))

    # קבלת נתונים מהשרת
    received_data = client_socket.recv(1024)  # קבלת עד 1024 בתים

    # פענוח הנתונים מ-JSON
    decoded_data = json.loads(received_data.decode("utf-8"))

    print(decoded_data)

    position_player = decoded_data[0][0]
    num_player = decoded_data[0][1]
    treasure_place = decoded_data[1]

    # הפעלת המשחק
    app = game.Game(
        treasure_place=treasure_place,
        position=position_player,
        num_player=num_player,
        client_socket=client_socket,
    )

    app.run()  # הפעלת המשחק
else:
    print("Failed to discover server.")
