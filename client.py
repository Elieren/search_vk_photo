import socket
import ssl

client = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), keyfile='server.key', certfile='server.crt') #Initialize the SSL protocol
client.connect(('', 9090))

file = open(f'{input("Path to photo: ")}', mode='rb') #Path to file
data_byte = file.read(1024)
while data_byte:
    #Sending photo byte code
    client.send(data_byte)
    data_byte = file.read(1024)
    if not data_byte:
        client.send('end'.encode())

result = client.recv(1024) #Getting data about a person
print()
print(result.decode('utf-8'))