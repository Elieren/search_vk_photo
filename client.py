import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('', 9090))

file = open(f'{input(": ")}', mode='rb')
data = file.read(1024)
while data:
    client.send(data)
    data = file.read(1024)
    if not data:
        client.send('end'.encode())

message = client.recv(1024)
print()
print(message.decode('utf-8'))