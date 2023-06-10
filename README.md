# search_face

for Linux

Тhis program downloads photos and user data from VK and searches for a person from your photo in real time.

## Creation of databases with user accounts.

In file search_id.py you need to insert your vk_token
```
python3 search_id.py
```
Create a database with user data (base.db)

## Download user photos (20 pieces)
```
python3 downloads_photo.py
```
Create a folder where all the photos are stored (id)

# Encode photo to database
```
python3 EncodeFace.py
```

Dataset_faces.dat and dataset_name.dat files will be created
## Search by photo
```
python3 search.py
```

## Live search by camera

### Start camera
```
python3 cam_search.py
```

# We use Nvidia Cuda.
Nvidia Cuda improves face detection accuracy.

To turn it on. Add text as written below.

```
face_recognition.face_locations(known_image) => face_recognition.face_locations(known_image, model='cnn')
```
In all files where face_locations is used.

## Other project implementations
[![server](https://img.shields.io/badge/Server_(Server_on_socket)-black?style=for-the-badge&logo=GitHub)](https://github.com/Elieren/search_vk_photo/tree/server)

[![server](https://img.shields.io/badge/Server_(Server_on_Flask)-black?style=for-the-badge&logo=GitHub)](https://github.com/Elieren/search_vk_photo/tree/API_server)