from search import * #Import search.py code
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

server = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt', server_side=True) #Initialize the SSL protocol
server.bind(('', 9090))
server.listen()
print("Server start.")

while True:
    try:
        #Getting the bytecode of a photo
        data_px = b''
        client, address = server.accept()

        data = client.recv(1024)
        while data:
            data_px = data_px + data
            data = client.recv(1024)
            if data[-3:] == b'end':
                break

        name = search(data_px) #Searching data by face
        print(name)
        name = '\n'.join(name)
        name = name.encode('utf-8')
        client.send(name) #Sending data to client
    except:
        pass
