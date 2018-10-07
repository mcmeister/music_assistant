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
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + '(Original Mix)' + codeClose)
else:
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName
            + '(' + mixName + ')' + codeClose)

# baseURL

url = 'https://mp3cc.biz/search/f/' + query + '/'

# proxy_headersRequest

req_proxy = RequestProxy()
req_proxy.generate_proxied_request(url)
print('\nConnecting to "Base URL"...\n')

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

req_proxy.generate_proxied_request(get_link)
print('\nConnecting to "Parsed URL"...\n')
shorten = Shortener('Tinyurl')
shrink_url = shorten.short(get_link)

# downloadShrinkURL

req_proxy.generate_proxied_request(shrink_url)
print('\nConnecting to "Shrink URL"...')
file = wget.download(shrink_url, out='/tmp')
print('\nDownloading: ' + '(' + query + ')' + ' via Short URL --> ' + shrink_url)
print('\nFile: ' + file + ' Downloaded!')

# editID3Tags

mp3 = MP3File(file)
mp3.set_version(VERSION_BOTH)
mp3.artist = artistName
mp3.song = songName
mp3.album = 'Telegram'
mp3.save()

# telegramBot

audio = open(file, 'rb')
token = 'my_token'
chat_id = '@my_chat_id'
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

# messCleaner

import cleaner
