import json
import socket
import game
from setting import *


# יצירת סוקט וניסיון להתחבר לשרת
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))  # התחברות לשרת

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
