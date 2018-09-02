## Music Assistant HTML parser

import requests
from bs4 import BeautifulSoup

a = input('Artist: ')
b = input('Name: ')
c = input('Remix("Enter" for blank): ')
s = str()

if c == s:
    query = (a + '_-_' + b)
else:
    query = (a + '_-_' + b + '_-_' + c)

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

url = 'http://mp3guild.com/mp3/' +query +'.html'

response = requests.get(url, headers=headers, stream=True)

handle = open('test.txt', "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        handle.write(chunk)

##file = open("test.txt", "w+")
##file.write(response.text)
##file.close()

soup = BeautifulSoup(open('test.txt'), 'html.parser')
print(soup.prettify())