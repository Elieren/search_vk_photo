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
	id_acc = pickle.load(file)

connect = sqlite3.connect('base.db') #Connecting to an existing database
cursor = connect.cursor()

def search_person_info(id_person):
    """Search for user information by id"""
    cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_person}';""")
    person_info = cursor.fetchone()
    return person_info

def search(data_image):
    """Getting data about a person"""
    fases = []
    id_vk = []
    inform_list = []

    image = PIL.Image.open(BytesIO(data_image))
    facesCurFrame = face_recognition.face_locations(np.array(image))
    faces_encoding = face_recognition.face_encodings(np.array(image), facesCurFrame)
    if faces_encoding != []:
        for face_encoding in faces_encoding:
            i = 0
            while True:
                try:
                    encoding = encodeListKnown[i]
                    results = face_recognition.compare_faces([face_encoding], encoding)

                    if results[0] == True:
                        id_person = id_acc[i]
                        if id_person not in id_vk:
                            id_vk.append(id_person)
                    else:
                        pass

                    i += 1
                except:
                    break

        if id_vk != []:
            for x in id_vk:
                person_info = search_person_info(x)
                inform_list.append(f'🟢 id: {x}, Name: {person_info[1]}, Bdate: {person_info[2]}, City: {person_info[3]}, Country: {person_info[4]}')
        else:
            inform_list.append('🟡 Not Found')
    else:
        inform_list.append('🔴 Face not found')
    return inform_list