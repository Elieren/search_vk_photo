from search import *
import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 9090))
server.listen()
print("Server start.")

while True:
    client, address = server.accept()

    try:
        os.remove('test.jpg')
    except:
        pass

    file = open('test.jpg', mode='wb')
    data = client.recv(1024)
    while data:
        file.write(data)
        data = client.recv(1024)
        if data[-3:] == b'end':
            break
    file.close()

    name = search('test.jpg')
    print(name)
    name = '\n'.join(name)
    name = name.encode('utf-8')
    client.send(name)