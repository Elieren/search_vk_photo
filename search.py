import face_recognition
import os
import re
import sqlite3
import pickle

with open('dataset_faces.dat', 'rb') as file:
	encodeListKnown = pickle.load(file)

with open('dataset_name.dat', 'rb') as file:
	id_acc = pickle.load(file)

id_vk = []
i = 0

connect = sqlite3.connect('base.db') #Connecting to an existing database
cursor = connect.cursor()


def search_person_info(id_person):
    """Search for user information by id"""
    cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_person}';""")
    person_info = cursor.fetchone()
    return person_info


direct = str(input("Path to photo: ")) #Path to photo
known_image = face_recognition.load_image_file(direct)
facesCurFrame = face_recognition.face_locations(known_image)
face_encoding = face_recognition.face_encodings(known_image, facesCurFrame)[0]


while True:
    #Finds a face match
    try:
        encoding = encodeListKnown[i]
        results = face_recognition.compare_faces([face_encoding], encoding)

        if results[0] == True:
            id_person = id_acc[i]
            if id_person not in id_vk:
                print('+')
                id_vk.append(id_person)
        else:
            pass

        i += 1
    except:
        break

if id_vk != []:
    #If the list is not empty, display the data of the matched users
    for x in id_vk:
        person_info = search_person_info(x)
        print(
            '\n', f'id: {x}, Name: {person_info[1]}, Bdate: {person_info[2]}, City: {person_info[3]}, Country: {person_info[4]}')
else:
    print('Not Found')
