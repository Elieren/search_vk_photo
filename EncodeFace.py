import numpy as np
import sqlite3
import face_recognition
import cv2
import os
import re
import pickle
from progress.bar import IncrementalBar

choice = str(input('Append (all/one): '))

if choice == 'all':
    fases = []
    images = []

    for dirpath, dirnames, filenames in os.walk("./id/"):
        for filename in filenames:
            fases.append(f'{dirpath}/{filename}')

    bar = IncrementalBar('Progress encode', max=len(fases)) #Create a progress bar

    for x in fases:
        Img = cv2.imread(x)
        images.append(Img)


    def Encodings(images, fases):
        """Decoding faces to work with Face_recognition"""
        encodeList = []
        name = []
        i = 0
        for img in images:
            try:
                img_e = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                facesCurFrame = face_recognition.face_locations(img_e)
                encode = face_recognition.face_encodings(img_e, facesCurFrame)[0]
                encodeList.append(encode)
                id_p = re.split('/', fases[i])
                p = id_p[2]
                name.append(p)
            except:
                pass
            bar.next()
            i += 1
        return encodeList, name


    encodeListKnown, name = Encodings(images, fases)
    bar.finish()

    #Saving data in pickle files
    with open('dataset_faces.dat', 'wb') as file:
        pickle.dump(encodeListKnown, file)

    with open('dataset_name.dat', 'wb') as file:
        pickle.dump(name, file)

elif choice == 'one':
    connect = sqlite3.connect('base.db') #Connecting to an existing database
    cursor = connect.cursor()

    with open('dataset_faces.dat', 'rb') as file:
        encodeListKnown = pickle.load(file)

    with open('dataset_name.dat', 'rb') as file:
        name = pickle.load(file)

    fold = str(input('Path to photo: '))
    id_person = str(input('id: '))
    name_a = str(input('name: '))
    bdata = str(input('bdata: '))
    city = str(input('city: '))
    country = str(input('country: '))

    Img = cv2.imread(fold)
    img_e = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
    
    #Encoding a face for Face_recognition
    try:
        encode = face_recognition.face_encodings(img_e)[0]
        encodeListKnown.append(encode)
        name.append(id_person)
    except:
        pass
    
    #Adding a new user to the databas
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)",
                   (id_person, name_a, bdata, city, country, 'not'))
    connect.commit()

    with open('dataset_faces.dat', 'wb') as file:
        pickle.dump(encodeListKnown, file)

    with open('dataset_name.dat', 'wb') as file:
        pickle.dump(name, file)

else:
    print('Error')