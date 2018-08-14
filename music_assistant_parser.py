## Music assistant HTML parser

import requests

a = input('Artist: ')
b = input('Name: ')
c = input('Remix("Enter" for blank): ')

query = (a + ' ' + b + ' ' + c + ' ' + 'mp3')
response = requests.get('http://promodj.com/search?searchfor=' + query)
print(response.url)