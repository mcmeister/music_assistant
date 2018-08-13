## We're going to search for music
## Download as mp3-file
## And upload to Telegram channel
## Let's Go! :)
## 12.08.2018 @ 4:03

from googlesearch import search

a = input('Artist: ')
b = input('Name: ')

query = (a + ' ' + b + ' ' + 'mp3')
for url in search(query, stop=10):
     print(url)
