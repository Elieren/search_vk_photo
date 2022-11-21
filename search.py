import face_recognition
import os
import re
import sqlite3
import pickle

fases = []
id_vk = []

with open('dataset_faces.dat', 'rb') as file:
	encodeListKnown = pickle.load(file)

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

def search(id_vk):
	cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_vk}';""")
	us = cursor.fetchone()
	return us

direct = str(input(": "))
known_image = face_recognition.load_image_file(direct)
face_encoding = face_recognition.face_encodings(known_image)[0]

for encoding in encodeListKnown:
    results = face_recognition.compare_faces([face_encoding], encoding)

    if results[0] == True:
        id_p = re.split('/', x)
        p = id_p[2]
        if p not in id_vk:
            print('+')
            id_vk.append(p)
        
    else:
        pass

if id_vk != []:
    for x in id_vk:
        us = search(x)
        print('\n',f'id: {x}, Name: {us[1]}, Bdate: {us[2]}, City: {us[3]}, Country: {us[4]}')
else:
    print('Not Found')
