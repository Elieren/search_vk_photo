import face_recognition
import os
import re
import sqlite3
import pickle

with open('dataset_faces.dat', 'rb') as file:
	encodeListKnown = pickle.load(file)

with open('dataset_name.dat', 'rb') as file:
	name = pickle.load(file)

fases = []
id_vk = []
a = 0

connect = sqlite3.connect('base.db')
cursor = connect.cursor()


def search(id_vk):
	cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_vk}';""")
	us = cursor.fetchone()
	return us


direct = str(input("Path to photo: "))
known_image = face_recognition.load_image_file(direct)
facesCurFrame = face_recognition.face_locations(known_image)
face_encoding = face_recognition.face_encodings(known_image, facesCurFrame)[0]


while True:
    try:
        encoding = encodeListKnown[a]
        results = face_recognition.compare_faces([face_encoding], encoding)

        if results[0] == True:
            p = name[a]
            if p not in id_vk:
                print('+')
                id_vk.append(p)
        else:
            pass

        a += 1
    except:
        break

if id_vk != []:
    for x in id_vk:
        us = search(x)
        print(
            '\n', f'id: {x}, Name: {us[1]}, Bdate: {us[2]}, City: {us[3]}, Country: {us[4]}')
else:
    print('Not Found')
