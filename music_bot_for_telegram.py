## We're going to search for music
## Download as mp3-file
## And upload to Telegram channel
## Let's Go! :)
## 12.08.2018 @ 4:03

from googlesearch import search
from html.parser import HTMLParser
import urllib.request as urllib2

a = input('Исполнитель: ')
b = input('Название: ')

query = (a + ' ' + b + '.mp3')
for url in search(query, stop=10):
     print(url)
