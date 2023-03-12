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

# We use Nvidia Cuda.
Nvidia Cuda improves face detection accuracy.

To turn it on. Add text as written below.

```
face_recognition.face_locations(np.array(im)) => face_recognition.face_locations(np.array(im), model='cnn')
```

## The program uses ssl encryption.
For the server to work, you need to generate an ssl certificate.

```
openssl genrsa -des3 -out server.key 1024

openssl req -new -key server.key -out server.csr

cp server.key server.key.org

openssl rsa -in server.key.org -out server.key

openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```
Certificates 'server.key' and 'server.crt' must be placed in the same folder as server.py