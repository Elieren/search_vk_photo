import numpy as np
import face_recognition
import cv2
import os
import re
import pickle

fases = []
images = []

for dirpath, dirnames, filenames in os.walk("./id/"):
    for filename in filenames:
        fases.append(f'{dirpath}/{filename}')

for x in fases:
    Img = cv2.imread(x)
    images.append(Img)


def Encodings(images):
    encodeList = []
    try:
        for img in images:
            img_e = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img_e)[0]
                encodeList.append(encode)
            except:
                pass
    except:
        pass
    return encodeList


encodeListKnown = Encodings(images)

with open('dataset_faces.dat', 'wb') as file:
    pickle.dump(encodeListKnown, file)
