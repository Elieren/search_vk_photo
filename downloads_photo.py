import sqlite3
import re
import os
import requests
import face_recognition

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

cursor.execute('SELECT * FROM users;')

results = cursor.fetchall()

os.mkdir("id")

a = len(results)
for i in range(a):
    try:
        p = 1
        a = 0
        id_vk = results[i][0]
        url_img = results[i][5]
        if url_img != 'Not':
            img = re.split(" !@! ", url_img)
            k = ("".join("%09d" % id_vk))
            os.mkdir(f'id/{k}')
            for c in img:
                jpg_bytes = requests.get(c).content
                with open(f'id/{k}/{p}.jpg', 'wb') as file:
                    file.write(jpg_bytes)
                a += 1
                image = face_recognition.load_image_file(f'id/{k}/{p}.jpg')
                face_locations = face_recognition.face_locations(image)
                if face_locations == []:
                    os.remove(f'id/{k}/{p}.jpg')
                    a -= 1
                else:
                    pass
                
                print(f'id/{k}/{p}.jpg')
                p += 1
            if a == 0:
                os.rmdir(f'id/{k}')
            else:
                pass
    except:
        continue