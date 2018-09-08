## Music Assistant HTML parser

import requests
import urllib2
from bs4 import BeautifulSoup
import wget

artistName = input('Artist: ')
songName = input('Name: ')
mixName = input('Mix(Blank for Original): ')
blank = str()

if mixName == blank:
    query = (artistName + '_-_' + songName)
else:
    query = (artistName + '_-_' + songName + '_-_' + mixName)

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

url = 'http://mp3guild.com/mp3/'+query+'.html'

response = requests.get(url, headers=headers, stream=True)

handle = open('test.txt', "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        handle.write(chunk)

soup = BeautifulSoup(open('test.txt'), 'html.parser')
for link in soup.find_all('a'):
    url = link.get('href')
    print(url)