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
from mp3_tagger import MP3File, VERSION_BOTH
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

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
print(banner + '\n')

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
print('\nNew filename gonna be: ' + newName + '\n')

# baseURL

url = 'https://mp3cc.biz/search/f/' + query + '/'

# proxy_headersRequest

req_proxy = RequestProxy()

req1 = req_proxy.generate_proxied_request(url)
if not req1:
    print('\nNext proxy... Base URL')
else:
    print('\nConnected to Base URL!')
    pass

# saveToFile

with open('parse.txt', 'wb') as f:
    response = requests.get(url)
    f.write(response.content)

# parseFromFile

with open('parse.txt', 'r', encoding='UTF-8') as p:
    s = BeautifulSoup(p, 'html.parser')
    link = s.find(href=re.compile('download'))
    get_link = link.get('href')

# shrinkParsedURL

access_token = "44e124bc4dba4890ded9e039fb9babb900086723"
tinyurl_short = Shortener('Tinyurl')
bitly_short = Shortener('Bitly', bitly_token=access_token)

req2 = req_proxy.generate_proxied_request(get_link)
if not req2:
    print('\nNext proxy... Parsed URL')
else:
    print('\nConnected to Parsed URL!')
    pass

shrink_url = bitly_short.short(get_link)
if not shrink_url:
    shrink_url = tinyurl_short.short(get_link)
    print('\nTinyurl: ' + str(shrink_url))
    pass
else:
    print('\nBitLy: ' + str(shrink_url))
    pass

# downloadShrinkURL

req3 = req_proxy.generate_proxied_request(shrink_url)
if not req3:
    print('\nNext proxy... Shrink URL')
else:
    print('\nConnected to Shrink URL!')
    pass

print('\nDownloading: ' + query + ' via Short URL --> ' + shrink_url)
file = wget.download(shrink_url, out='/tmp')
print('\nFile: ' + file + ' Downloaded!\n')

# editID3Tags

mp3 = MP3File(file)
mp3.set_version(VERSION_BOTH)
mp3.artist = artistName
mp3.song = songName
mp3.album = 'Telegram'
mp3.save()
tags = mp3.get_tags()
print(tags)

# telegramBot

os.rename(str(file), newName)
audio = open(newName, 'rb')
token = '658217975:AAEsRGGeVoArqhuEH4D_-iw5qok45fi6aM8'
chat_id = '@testing_now'
tb = telebot.TeleBot(token)
tb_status = str(tb.get_me())
print('\nStatus: ' + tb_status)

# uploadFile

print('\nUploading File to a Telegram Channel: ' + chat_id)
tb.send_audio(chat_id, audio)
tb.send_message(chat_id, text, parse_mode="HTML")
print('\nFile Uploaded!')

# statusImprint

print('\nFound: ' + query)
print('\nDownloaded: ' + query)
print('\nUploaded to: ' + chat_id)

import cleaner