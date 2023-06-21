import sqlite3
import re
import os
import requests
import face_recognition

connect = sqlite3.connect('base.db') #Connecting to an existing database
cursor = connect.cursor()

cursor.execute('SELECT * FROM users;')

results = cursor.fetchall()

os.mkdir("id")

results_len = len(results) #Number of profiles
for i in range(results_len):
    try:
        image_index = 1
        quantity_images = 0
        id_vk = results[i][0] #Get profile id
        url_img = results[i][5] #Get photos url
        if url_img != 'Not':
            imgs = re.split(" !@! ", url_img)
            id_person = ("".join("%09d" % id_vk))
            os.mkdir(f'id/{id_person}')
            for img_url in imgs:
                jpg_bytes = requests.get(img_url).content #Downloading a photo
                with open(f'id/{id_person}/{image_index}.jpg', 'wb') as file:
                    file.write(jpg_bytes)
                quantity_images += 1
                #Checking for the presence of faces in the photo
                image = face_recognition.load_image_file(f'id/{id_person}/{image_index}.jpg')
                face_locations = face_recognition.face_locations(image)
                if (face_locations == []) or (len(face_locations) > 1):
                    os.remove(f'id/{id_person}/{image_index}.jpg')
                    quantity_images -= 1
                else:
                    pass
                
                print(f'id/{id_person}/{image_index}.jpg')
                image_index += 1
            if quantity_images == 0:
                os.rmdir(f'id/{id_person}')
            else:
                pass
    except:
        continue