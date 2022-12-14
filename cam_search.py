import numpy as np
import face_recognition
import cv2
import os
import re
import sqlite3
import pickle

name = []
namd = []
mam = []

with open('dataset_faces.dat', 'rb') as file:
	encodeListKnown = pickle.load(file)

with open('dataset_name.dat', 'rb') as file:
	name = pickle.load(file)

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

def search(id_vk):
	cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_vk}';""")
	us = cursor.fetchone()
	return us

def nick(name_a):
    global namd
    for x in name_a:
        if x not in namd:
            us = search(x)
            print(
                '\n', f'id: {x}, Name: {us[1]}, Bdate: {us[2]}, City: {us[3]}, Country: {us[4]}')
            namd.append(x)
        else:
            pass
    for x in namd:
        if x not in name_a:
            namd.remove(x)
            print(' id:', x, 'leave')


print(name)
print("I'm listening")

cap = cv2.VideoCapture('1.mp4')

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    nick(mam)
    mam = []

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name_a = str((name[matchIndex]))
            mam.append(name_a)
            #print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name_a, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            name_a = 'Not'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                          (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name_a, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("WebCam", img)
    cv2.waitKey(1)
