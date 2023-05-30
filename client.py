import socket
import ssl

client = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt') #Initialize the SSL protocol
client.connect(('', 9090))

file = open(f'{input("Path to photo: ")}', mode='rb') #Path to file
data = file.read(1024)
while data:
    #Sending photo byte code
    client.send(data)
    data = file.read(1024)
    if not data:
        client.send('end'.encode())

message = client.recv(1024) #Getting data about a person
print()
print(message.decode('utf-8'))