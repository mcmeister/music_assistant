## Music Assistant HTML parser

import requests

a = input('Artist: ')
b = input('Name: ')
c = input('Remix("Enter" for blank): ')

query = (a + '_' + b + '_' + c)
response = requests.get('http://mp3guild.com/mp3/' + query)
song = response.url
print(song)