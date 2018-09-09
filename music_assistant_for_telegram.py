'''
We're going to search for the music(done)
Download track as mp3-file(done)
And upload it to Telegram channel(done)
Let's Go! :)
12.08.2018 @ 4:03
All done! 09.09.2018 @ 18:09
'''

import re
import sys
import wget
import telebot
import requests
from bs4 import BeautifulSoup

## User Input Section

artistName = input('Artist: ')
songName = input('Name: ')
mixVer = input('Mix Version(Blank for Original): ')
blank = str() ## String Variable for blank input

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
    print('Downloading File...')
    mp3 = wget.download(file)
    print('Download Complete!')

## Telegram Bot Section

TOKEN = 'my_token'
tb = telebot.TeleBot(TOKEN)
chat_id = '@my_channel'
audio = open(mp3, 'rb')
user = tb.get_me()

## Send audio file to Telegram Channel

print('Uploading to Music Meister Channel...')
tb.send_audio(chat_id, audio)
print('File Upload Completed!')

## Send message to Telegram Channel

if mixVer == blank:
    text = (artistName + ' - ' + songName)
else:
    text = (artistName + ' - ' + songName + '(' + mixVer + ')')

tb.send_message(chat_id, text)

tb.polling()
sys.exit("Everything Done!")
