## Docker-Server

## Подготовка к build 
### The program uses ssl encryption.

For the server to work, you need to generate an ssl certificate.
```
openssl genrsa -des3 -out server.key 2048

openssl req -new -key server.key -out server.csr

cp server.key server.key.org

openssl rsa -in server.key.org -out server.key

openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
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

## Docker

Build docker file
```
docker build . -t search_face
```
Run server
```
docker run -d -p 9090:9090 search_face
```