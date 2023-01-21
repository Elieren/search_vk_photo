import face_recognition
import os
import re
import sqlite3
import pickle
import cv2
import PIL.Image
from io import BytesIO
import numpy as np

with open('dataset_faces.dat', 'rb') as file:
	encodeListKnown = pickle.load(file)

with open('dataset_name.dat', 'rb') as file:
	name = pickle.load(file)

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

def search_a(id_vk):
	cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_vk}';""")
	us = cursor.fetchone()
	return us

def search(x):
    fases = []
    id_vk = []
    name_a = []

    im = PIL.Image.open(BytesIO(x))
    face_encoding_1 = face_recognition.face_encodings(np.array(im))
    if face_encoding_1 != []:
        for face_encoding in face_encoding_1:
            a = 0
            while True:
                try:
                    encoding = encodeListKnown[a]
                    results = face_recognition.compare_faces([face_encoding], encoding)

                    if results[0] == True:
                        p = name[a]
                        if p not in id_vk:
                            id_vk.append(p)
                    else:
                        pass

                    a += 1
                except:
                    break

        if id_vk != []:
            for x in id_vk:
                us = search_a(x)
                name_a.append(f'🟢 id: {x}, Name: {us[1]}, Bdate: {us[2]}, City: {us[3]}, Country: {us[4]}')
        else:
            name_a.append('🟡 Not Found')
    else:
        name_a.append('🔴 Face not found')
    return name_a
