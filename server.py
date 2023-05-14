from search import *
import socket
import os
import sys
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
server = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_side=True)
server.bind(('0.0.0.0', 9090))
server.listen()

while True:
    try:
        data_px = b''
        client, address = server.accept()

        data = client.recv(1024)
        while data:
            data_px = data_px + data
            data = client.recv(1024)
            if data[-3:] == b'end':
                break

        name = search(data_px)
        print(name)
        name = '\n'.join(name)
        name = name.encode('utf-8')
        client.send(name)
    except:
        pass
