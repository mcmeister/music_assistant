## Music Assistant HTML parser

import requests

a = input('Artist: ')
b = input('Name: ')
c = input('Remix("Enter" for blank): ')
s = str()

if c == s:
    query = (a + '_-_' + b)
else:
    query = (a + '_-_' + b + '_-_' + c)

url = 'http://mp3guild.com/mp3/' + query + '.html'
r = requests.get(url)
with open('request.html', 'w') as output_file:
    output_file.write(r.text.encode('cp1251'))
