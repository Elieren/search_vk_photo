# search_face

for Linux

## Server and client
Before work, you need to edit the client and server files
```
nano server.py
```
server.bind(('', 9090)) => server.bind(('your ip', 9090))
Save and exit
```
nano client.py
```
client.connect(('', 9090)) => client.connect(('server ip', 9090))
Save and exit

### Start server
```
python3 server.py
```
### Start client
```
python3 client.py
```

## !
Port 9090