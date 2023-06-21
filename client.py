import requests
import os
import json

ip_server = '' #Flask server

path = str(input("Path to photo: "))
path_a = os.path.split(path)[-1]
format_file = path_a.split('.')[-1]

# Открываем файл изображения
with open(path, "rb") as image_file:
    # создаем данные формы для отправки файла
    files = {'image': (path_a, image_file, f'image/{format_file}')}

    # передаем данные формы в запрос
    response = requests.post(f'{ip_server}/api', files=files, verify=False, cert=('server.crt','server.key'))

# получаем ответ от сервера
result = response.json()
for i in result:
    print(json.loads(i))