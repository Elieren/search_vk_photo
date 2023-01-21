from search import *
import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.161', 9090))
server.listen()
print("Server start.")

while True:
    data_px = b''
    client, address = server.accept()

    data = client.recv(1024)
    while data:
        data_px = data_px + data
        data = client.recv(1024)
        if data[-3:] == b'end':
            break
    file.close()

    name = search(data_px)
    print(name)
    name = '\n'.join(name)
    name = name.encode('utf-8')
    client.send(name)