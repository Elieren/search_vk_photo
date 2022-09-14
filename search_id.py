import sqlite3
import json
from bs4 import BeautifulSoup
import lxml
import requests
import re

connect = sqlite3.connect('orders.db')
cursor = connect.cursor()

access_token = 'c0327326225b38a1107014a3c02b4e3b2415ee699d670785cba4ffa293e68a8e188155189110da611a100'
api_version = '5.89'

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
   id_vk INT PRIMARY KEY,
   name TEXT,
   bdate TEXT,
   city TEXT,
   country TEXT,
   img_url TEXT);
""")

def nick_name(k):
   try:
      name = k['first_name']+' '+k['last_name']
   except:
      name = "Not"
   return name

def day_b(k):
   try:
      bdate = k['bdate']
   except:
      bdate = "Not"
   return bdate

def strana(k):
   try:
    city = k['city']['title']
   except:
      city = 'Not'

   try:
      country = k['country']['title']
   except:
      country = 'Not'
   
   return city, country

def img(url_adress, access_token, api_version):
   try:
      links = []
      e = requests.get(f'https://api.vk.com/method/photos.getAll?owner_id={url_adress}&access_token={access_token}&v={api_version}').text
      e = json.loads(e)['response']['items']
      for x in e:
         k = x['sizes'][-1]['url']
         links.append(k)
      url_img = ' !@! '.join(links)
   except:
      url_img = "Not"
   return url_img

def add(url_adress, nick, b, city, country, link_image, cursor):
	cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)",(url_adress, nick, b, city, country, link_image))
	connect.commit()

for x in range(1 ,100000000):
   url_adress = ("".join("%09d" % x ))
   print(url_adress)
   p = requests.get(f'https://api.vk.com/method/users.get?user_ids={url_adress}&fields=bdate,city,country&access_token={access_token}&v={api_version}').text

   k = json.loads(p)['response'][0]
   nick = nick_name(k)
   b = day_b(k)
   city, country = strana(k)
   link_image = img(url_adress, access_token, api_version)
   add(url_adress, nick, b, city, country, link_image, cursor)
