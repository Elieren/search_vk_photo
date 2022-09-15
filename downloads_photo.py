import sqlite3
import re
import os
import requests

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

cursor.execute('SELECT * FROM users;')

results = cursor.fetchall()

os.mkdir("id")

a = len(results)
for i in range(a):
    p = 1
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
            p += 1
