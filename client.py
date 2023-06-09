import requests
import os
import json

path = str(input("Path to photo: "))
path_a = os.path.split(path)[-1]
format_file = path_a.split('.')[-1]

# Открываем файл изображения
with open(path, "rb") as image_file:
    # создаем данные формы для отправки файла
    files = {'image': (path_a, image_file, f'image/{format_file}')}

    # передаем данные формы в запрос
    response = requests.post("http://127.0.0.1:5000/api", files=files)

# получаем ответ от сервера
a = response.json()
for i in a:
    print(json.loads(i))