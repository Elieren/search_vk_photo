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
        data_byte_line= b''
        client, address = server.accept()

        data_byte = client.recv(1024)
        while data:
            data_byte_line = data_byte_line + data_byte
            data_byte = client.recv(1024)
            if data_byte[-3:] == b'end':
                break

        info = search(data_byte_line) #Searching data by face
        print(info)
        info = '\n'.join(info)
        info = info.encode('utf-8')
        client.send(info) #Sending data to client
    except:
        pass
