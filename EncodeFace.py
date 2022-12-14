import numpy as np
import sqlite3
import face_recognition
import cv2
import os
import re
import pickle
from progress.bar import IncrementalBar

serv = str(input('Append (all/one): '))

if serv == 'all':
    fases = []
    images = []

    for dirpath, dirnames, filenames in os.walk("./id/"):
        for filename in filenames:
            fases.append(f'{dirpath}/{filename}')

    bar = IncrementalBar('Progress encode', max=len(fases))

    for x in fases:
        Img = cv2.imread(x)
        images.append(Img)


    def Encodings(images, fases):
        encodeList = []
        name = []
        l = 0
        for img in images:
            img_e = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img_e)[0]
                encodeList.append(encode)
                id_p = re.split('/', fases[l])
                p = id_p[2]
                name.append(p)
            except:
                pass
            bar.next()
            l += 1
        return encodeList, name


    encodeListKnown, name = Encodings(images, fases)
    bar.finish()

    with open('dataset_faces.dat', 'wb') as file:
        pickle.dump(encodeListKnown, file)

    with open('dataset_name.dat', 'wb') as file:
        pickle.dump(name, file)

elif serv == 'one':
    connect = sqlite3.connect('base.db')
    cursor = connect.cursor()

    with open('dataset_faces.dat', 'rb') as file:
        encodeListKnown = pickle.load(file)

    with open('dataset_name.dat', 'rb') as file:
        name = pickle.load(file)

    fold = str(input('Path to photo: '))
    id_a = str(input('id: '))
    name_a = str(input('name: '))
    bdata = str(input('bdata: '))
    city = str(input('city: '))
    country = str(input('country: '))

    Img = cv2.imread(fold)
    img_e = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)

    try:
        encode = face_recognition.face_encodings(img_e)[0]
        encodeListKnown.append(encode)
        name.append(id_a)
    except:
        pass

    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)",
                   (id_a, name_a, bdata, city, country, 'not'))
    connect.commit()

    with open('dataset_faces.dat', 'wb') as file:
        pickle.dump(encodeListKnown, file)

    with open('dataset_name.dat', 'wb') as file:
        pickle.dump(name, file)

else:
    print('Error')