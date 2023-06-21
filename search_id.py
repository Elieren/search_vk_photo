import sqlite3
import json
from bs4 import BeautifulSoup
import lxml
import requests
import re

connect = sqlite3.connect('base.db') #Database creation
cursor = connect.cursor()

access_token = '' #Vk_token
api_version = '5.89'

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
   id_vk INT NOT NULL PRIMARY KEY,
   name TEXT NOT NULL,
   bdate TEXT,
   city TEXT,
   country TEXT,
   img_url TEXT NOT NULL
   );
""")

def nick_name(k):
   """Getting a first and last name"""
   try:
      name = k['first_name']+' '+k['last_name']
   except:
      name = "Not"
   return name

def day_b(k):
   """Getting date of birth"""
   try:
      bdate = k['bdate']
   except:
      bdate = "Not"
   return bdate

def strana(k):
   """Getting city and country"""
   try:
    city = k['city']['title']
   except:
      city = 'Not'

   try:
      country = k['country']['title']
   except:
      country = 'Not'
   
   return city, country

def img(id_user_vk, access_token, api_version):
   """Getting photos"""
   try:
      links = []
      result = requests.get(f'https://api.vk.com/method/photos.getAll?owner_id={id_user_vk}&access_token={access_token}&v={api_version}').text
      result = json.loads(result)['response']['items']
      for i in result:
         image_url = i['sizes'][-1]['url']
         links.append(image_url)
      url_img = ' !@! '.join(links)
      status = True
   except:
      url_img = "Not"
      status = False
   return url_img, status

def add(id_user_vk, nick, bdate, city, country, link_image, cursor):
   """Adding received data to the database"""
   cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)",(id_user_vk, nick, bdate, city, country, link_image))
   connect.commit()

for x in range(1 ,100000000):
   id_user_vk = ("".join("%09d" % x ))
   print(id_user_vk)
   result_id = requests.get(f'https://api.vk.com/method/users.get?user_ids={id_user_vk}&fields=bdate,city,country&access_token={access_token}&v={api_version}').text

   data = json.loads(result_id)['response'][0]
   nick = nick_name(data)
   bdate = day_b(data)
   city, country = strana(data)
   link_image, status = img(id_user_vk, access_token, api_version)
   if stauts == True:
         add(id_user_vk, nick, bdate, city, country, link_image, cursor)
   else:
      pass
