import sqlite3
import json
from bs4 import BeautifulSoup
import lxml
import requests
import re

connect = sqlite3.connect('orders.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
   id_vk INT PRIMARY KEY,
   name TEXT,
   img_url TEXT);
""")

def nick_name(soup):
   block = soup.find_all("title")
   for x in block:
      name = str(x)
   reko = name.replace('|', '!')
   nick = re.split(">| !", reko)
   if 'ВКонтакте' in nick[1]:
      x = "Not exist"
      return x
   else:
      return nick[1]

def img(soup, url_adress):
   a = []
   links = []
   block = soup.find_all("a", href=True)
   for link in block:
      a.append(link['href'])
   for x in a:
      if f'/photo' in x:
         links.append(x)
   url_img = '|'.join(links)
   return url_img

def add(url_adress, nick, link_image, cursor):
	cursor.execute("INSERT INTO users VALUES(?, ?, ?)",(url_adress, nick, link_image))
	connect.commit()

for x in range(1 ,10000000000):
   url_adress = ("".join("%09d" % x ))
   url = f"https://vk.com/id{url_adress}"
   responce = requests.get(url).text
   soup = BeautifulSoup(responce, 'lxml')

   nick = nick_name(soup)
   link_image = img(soup, url_adress)
   add(url_adress, nick, link_image, cursor)
