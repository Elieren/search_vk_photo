from search import *
import socket
import os
import sys
import ssl

banner = '''
███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
'''
print(banner)

server = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), 'server.key', 'server.crt', True, ciphers="ADH-AES256-SHA")
server.bind(('', 9090))
server.listen()
print("Server start.")

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
