"""
We're going to search for the music(done)
Download track as mp3-file(done)
And upload it to Telegram channel(done)
Let's Go! :)
12.08.2018 @ 4:03
All done!
09.09.2018 @ 18:09
"""

# importInput

import os
import re
import wget
import telebot
import requests
from bs4 import BeautifulSoup
from pyshorteners import Shortener
from fake_useragent import UserAgent
from mp3_tagger import MP3File, VERSION_BOTH

# bannerInput

banner = '''
--------------------------------------------------------------------------------------------------
  __  __                 _                                   _         _                     _    
 |  \/  |               (_)              /\                 (_)       | |                   | |   
 | \  / |  _   _   ___   _    ___       /  \     ___   ___   _   ___  | |_    __ _   _ __   | |_  
 | |\/| | | | | | / __| | |  / __|     / /\ \   / __| / __| | | / __| | __|  / _` | | '_ \  | __| 
 | |  | | | |_| | \__ \ | | | (__     / ____ \  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_  
 |_|  |_|  \__,_| |___/ |_|  \___|   /_/    \_\ |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__| 
         FOR TELEGRAM           v.1.01b         by Viacheslav Vorotilin aka "music meister"      
--------------------------------------------------------------------------------------------------
'''
print(banner)

# userInput

artistName = input('Artist: ')      # Variable for Artist Name
songName = input('Name: ')          # Variable for Song Name
mixName = input('Remixed by: ')     # Variable for DJ Name
blankInput = str()                  # String Variable for Blank Input

# programInput

'''
plusInput = '+'                     # Variable for a Plus [+]
underInput = '_'                    # Variable for an Underscore [_]
'''
spaceInput = ' '                    # Variable for a Space [ ]
hyphenInput = '-'                   # Variable for a Hyphen [-]
codeOpen = '<code>'                 # Variable for Text-Formatting
codeClose = '</code>'               # Variable for Text-Formatting
boldOpen = '<b>'                    # Variable for Text-Formatting
boldClose = '</b>'                  # Variable for Text-Formatting

# cuteQueries

if mixName == blankInput:
    query = (artistName + spaceInput + songName)
elif songName == blankInput:
    query = (artistName + spaceInput + mixName)
elif artistName == blankInput:
    query = (songName + spaceInput + mixName)
else:
    query = (artistName + spaceInput + songName + spaceInput + mixName)
print('\nQuery: ' + query)

if mixName == blankInput:
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + codeClose)
else:
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName
            + '(' + mixName + ')' + codeClose)

if mixName == blankInput:
    newName = ('/tmp/' + artistName + hyphenInput + songName + '.mp3')
else:
    newName = ('/tmp/' + artistName + hyphenInput + songName + hyphenInput + mixName + '.mp3')

# baseURL

url = 'https://mp3cc.biz/search/f/' + query + '/'

# userAgent

ua = UserAgent()
ua.update()

# headers

headers = ua.random

# saveToFile

with open('parse.txt', 'wb') as f:
    response = requests.get(url, headers=headers)
    f.write(response.content)

# parseFromFile

with open('parse.txt', 'r', encoding='UTF-8') as p:
    s = BeautifulSoup(p, 'html.parser')
    link = s.find(href=re.compile('download'))
    get_link = link.get('href')

# shrinkParsedURL

access_token = 'my_bitly_token'
tinyurl_short = Shortener('Tinyurl')
bitly_short = Shortener('Bitly', bitly_token=access_token)

shrink_url = bitly_short.short(get_link)
if shrink_url:
    print('\nBitLy: ' + str(shrink_url))
else:
    shrink_url = tinyurl_short.short(get_link)
    print('\nTinyurl: ' + str(shrink_url))

# downloadShrinkURL

print('\nDownloading: ' + query + ' via Short URL --> ' + shrink_url)
file = wget.download(shrink_url, out='/storage/emulated/0/temp')
print('\nDownloaded!: ' + str(file))

# editID3Tags

mp3 = MP3File(file)
mp3.set_version(VERSION_BOTH)
mp3.artist = artistName
mp3.song = songName
mp3.album = 'Telegram'
mp3.publisher = ''
mp3.save()
tags = mp3.get_tags()
print(tags)

# telegramBot

print('\nFilename will be: ' + newName)
os.rename(str(file), newName)
audio = open(newName, 'rb')
token = 'my_bot_token'
chat_id = '@my_chat_id'
tb = telebot.TeleBot(token)
tb_status = str(tb.get_me())
print('\nStatus: ' + tb_status)

# uploadFile

print('\nUploading File to a Telegram Channel: ' + chat_id)
print('\nMessage will be: ' + str(text))
send = tb.send_audio(chat_id, audio)
message_id = send.message_id
caption = str(text)
tb.edit_message_caption(caption, chat_id, message_id, parse_mode='HTML')
print('\nFile Uploaded!')

# statusImprint

print('\nFound: ' + query)
print('\nDownloaded: ' + query)
print('\nUploaded to: ' + chat_id)

import cleaner_mob