import socket
import ssl

client = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt')
client.connect(('', 9090))

file = open(f'{input("Path to photo: ")}', mode='rb')
data = file.read(1024)
while data:
    client.send(data)
    data = file.read(1024)
    if not data:
        client.send('end'.encode())

message = client.recv(1024)
print()
print(message.decode('utf-8'))