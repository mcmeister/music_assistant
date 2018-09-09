## We're going to search for music(done) 
## Download as mp3-file(done)
## And upload to Telegram channel
## Let's Go! :)
## 12.08.2018 @ 4:03

import requests
import wget
import re
from bs4 import BeautifulSoup

## User Input Section

artistName = input('Artist: ')
songName = input('Name: ')
mixVer = input('Mix Version(Blank for Original): ')
blank = str() ## String Variable for blank input (Space)

## Appropriate to Website's Search Query (including or excluding Mix Version)

if mixVer == blank:
    query = (artistName + '_-_' + songName)
else:
    query = (artistName + '_-_' + songName + '_-_' + mixVer)

## Headers to access Website

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

## Appropriate url-string to access Website's Search

url = 'http://mp3guild.com/mp3/'+query+'.html'

## Save Search results to Text-File

response = requests.get(url, headers=headers, stream=True)
handle = open('parse.txt', "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        handle.write(chunk)

## Parse & Download mp3-link from Text-File

with open("parse.txt", "r") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    link = soup.find(href=re.compile("dl.php?"))
    file = link.get('href')
    wget.download(file)