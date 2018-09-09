## Music Assistant HTML parser

import requests
import re
from bs4 import BeautifulSoup
import wget

artistName = input('Artist: ')
songName = input('Name: ')
mixVer = input('Mix Version(Blank for Original): ')
blank = str()

if mixVer == blank:
    query = (artistName + '_-_' + songName)
else:
    query = (artistName + '_-_' + songName + '_-_' + mixVer)

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

url = 'http://mp3guild.com/mp3/'+query+'.html'

response = requests.get(url, headers=headers, stream=True)

handle = open('parse.txt', "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        handle.write(chunk)

with open("parse.txt", "r") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    link = soup.find(href=re.compile("dl.php?"))
    file = link.get('href')
    wget.download(file)