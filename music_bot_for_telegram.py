##We're going to find music track by artist - name
##Download it and upload to Telegram channel... 

from googlesearch import search

xx = input('Enter Artist - Name or Enter to finish: ')

query = xx + '.mp3'
mp3 = search(query, stop=50)
for url in mp3:
    print(url)
