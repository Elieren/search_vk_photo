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

## Encode photo to database
```
python3 EncodeFace.py
```

Dataset_faces.dat file will be created

## Search by photo
```
python3 search.py
```

## Live search by camera
```
python3 cam_search.py
```