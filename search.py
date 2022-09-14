import face_recognition
import os
import re
import sqlite3

fases = []
id_vk = []

connect = sqlite3.connect('orders.db')
cursor = connect.cursor()

def search(id_vk):
	cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_vk}';""")
	us = cursor.fetchone()
	return us

direct = str(input(": "))
known_image = face_recognition.load_image_file(direct)
face_encoding = face_recognition.face_encodings(known_image)[0]

for dirpath, dirnames, filenames in os.walk("./id/"):
    for filename in filenames:
        fases.append(f'{dirpath}/{filename}')

for x in fases:
    unknown_picture = face_recognition.load_image_file(x)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)

    if len(unknown_face_encoding) > 0:
        encoding = unknown_face_encoding[0]
        results = face_recognition.compare_faces([face_encoding], encoding)
    
        if results[0] == True:
            print('+')
            id_p = re.split('/', x)
            id_vk.append(id_p[2])
            
        else:
            pass

for x in id_vk:
    us = search(x)
    print('\n',f'id: {x}, Name: {us[1]}, Bdate: {us[2]}, City: {us[3]}, Country: {us[4]}')
