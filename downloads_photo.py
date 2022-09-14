import sqlite3
import re
import os
import requests

connect = sqlite3.connect('orders.db')
cursor = connect.cursor()

cursor.execute('SELECT * FROM users;')

results = cursor.fetchall()

p = 1
a = len(results)
for i in range(a):
    id_vk = results[i][0]
    url_img = results[i][5]
    if url_img != 'Not':
        img = re.split(" !@! ", url_img)
        k = ("".join("%09d" % id_vk))
        os.mkdir(k)
        for c in img:
            jpg_bytes = requests.get(c).content
            with open(f'{k}\\{p}.jpg', 'wb') as file:
                file.write(jpg_bytes)
            p += 1
