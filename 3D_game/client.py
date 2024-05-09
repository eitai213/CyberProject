import json
import socket
import setting as s
import game

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((s.SERVER_IP, s.SERVER_PORT))


# קבלת נתונים מהשרת
received_data = client_socket.recv(1024)  # קבלת עד 1024 בתים

# פענוח הנתונים מ-JSON לרשימה
decoded_data = json.loads(received_data.decode('utf-8'))

print("Received data:", decoded_data)

position_player = decoded_data[0][0]
num_player = decoded_data[0][1]
treasure_place = decoded_data[1]

app = game.Game(treasure_place=treasure_place, position=position_player, num_player=num_player, client_socket=client_socket)

app.run()