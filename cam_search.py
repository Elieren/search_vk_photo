import numpy as np
import face_recognition
import cv2
import os
import re
import sqlite3
import pickle

id_in_frame_arr = []
in_frame = []

with open('dataset_faces.dat', 'rb') as file:
	encodeListKnown = pickle.load(file)

with open('dataset_name.dat', 'rb') as file:
	name = pickle.load(file)

connect = sqlite3.connect('base.db') #Connecting to an existing database
cursor = connect.cursor()

def search_person_info(id_person):
    """Search for user information by id"""
    cursor.execute(f"""SELECT * FROM users WHERE id_vk = '{id_person}';""")
    person_info = cursor.fetchone()
    return person_info

def nick(persons):
    """Logging in and out of users"""
    global id_in_frame_arr
    for x in persons:
        if x not in id_in_frame_arr:
            person_info = search_person_info(x)
            print(
                '\n', f'id: {x}, Name: {person_info[1]}, Bdate: {person_info[2]}, City: {person_info[3]}, Country: {person_info[4]}')
            id_in_frame_arr.append(x)
        else:
            pass
    for x in id_in_frame_arr:
        if x not in persons:
            id_in_frame_arr.remove(x)
            print(' id:', x, 'leave')


print(name)
print("I'm listening")

cap = cv2.VideoCapture(0) #Getting video from the camera

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #Find faces in a photo
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    nick(in_frame)
    in_frame = []

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        #Comparison of a face with a list of faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            text_box = str((name[matchIndex]))
            in_frame.append(text_box)
            Green = 255
            Red = 0

        else:
            text_box = 'Not'
            Green = 0
            Red = 255

        #Draw a frame around the face
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, Green, Red), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                        (0, Green, Red), cv2.FILLED)
        cv2.putText(img, text_box, (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("WebCam", img)
    cv2.waitKey(1)
