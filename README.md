## API_server

## Under development

### Implemented:
- [x] Switch from socket to Flask (API)
- [x] Implement Flask support instead of socket for cli client and gui client
- [x] Implement support for ssl encryption
- [ ] Test client parts of the application

## Server and client
Before work, you need to edit the client
```
nano client.py
```
ip_server = '' --> ip_server = 'ip'

Save and exit

### Start server
```
python3 server.py
```
### Start client
__You must use the keys (.key, .crt) that are used for server.__
```
python3 client.py
```

# We use Nvidia Cuda.
Nvidia Cuda improves face detection accuracy.

To turn it on. Add text as written below.

```
face_recognition.face_locations(np.array(im)) => face_recognition.face_locations(np.array(im), model='cnn')
```

## The program uses ssl encryption.
For the server to work, you need to generate an ssl certificate.

```
openssl req \
    -newkey rsa:2048 \
    -nodes \
    -keyout server.key \
    -x509 \
    -days 365 \
    -out server.crt \
    -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/OU=MyDept/CN=myserver.com" \
    -addext "subjectAltName = DNS:localhost"
```
Certificates 'server.key' and 'server.crt' must be placed in the same folder as server.py

## Docker-Server

### Preparing for build
#### The program uses ssl encryption.

For the server to work, you need to generate an ssl certificate.
```
openssl req \
    -newkey rsa:2048 \
    -nodes \
    -keyout server.key \
    -x509 \
    -days 365 \
    -out server.crt \
    -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/OU=MyDept/CN=myserver.com" \
    -addext "subjectAltName = DNS:localhost"
```
Certificates 'server.key' and 'server.crt' must be placed in the same folder as server.py

### Packing additional files

Place the server.crt, server.key, base.db dataset_faces.dat and dataset_name.dat files in the server.py directory

```
search_vk_photo \
    base.db
    dataset_faces.dat
    dataset_name.dat
    Dockerfile
    README.md
    requirements.py
    search.py
    server.crt
    server.key
    server.py
```

To make the directory look like this

### Docker

Build docker file
```
docker build . -t search_face
```
Run server
```
docker run -d -p 5000:5000 search_face
```