"""
We're going to search for the music(done)
Download track as mp3-file(done)
And upload it to Telegram channel(done)
Let's Go! :)
12.08.2018 @ 4:03
All done!
09.09.2018 @ 18:09
"""

import re
import requests
import telebot
import wget
from bs4 import BeautifulSoup
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from mp3_tagger import MP3File, VERSION_BOTH
from pyshorteners import Shortener

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

# UserInput

artistName = input('Artist: ')  # Variable for Artist Name
songName = input('Name: ')      # Variable for Song Name
mixName = input('Mix Name: ')   # Variable for Remix Name
blankInput = str()              # String Variable for Blank Input

# ProgramInput

'''
plusInput = '+'                 # Variable for a Plus [+]
underInput = '_'                # Variable for an Underscore [_]
'''
spaceInput = ' '                # Variable for a Space [ ]
hyphenInput = '-'               # Variable for a Hyphen [-]
codeOpen = '<code>'             # Variable for Text-Formatting
codeClose = '</code>'           # Variable for Text-Formatting
boldOpen = '<b>'                # Variable for Text-Formatting
boldClose = '</b>'              # Variable for Text-Formatting

# CuteQueries

if mixName == blankInput:
    query = (artistName + spaceInput + songName)
elif songName == blankInput:
    query = (artistName + spaceInput + mixName)
elif artistName == blankInput:
    query = (songName + spaceInput + mixName)
else:
    query = (artistName + spaceInput + songName + spaceInput + mixName)

if mixName == blankInput:
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + codeClose)
else:
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName
            + spaceInput + '(' + mixName + ')' + codeClose)

url = 'https://mp3cc.biz/search/f/' + query + '/'

req_proxy = RequestProxy()
req_proxy.generate_proxied_request(url)

with open('parse.txt', 'wb') as f:
    response = requests.get(url)
    f.write(response.content)

with open('parse.txt', 'r', encoding='UTF-8') as p:
    s = BeautifulSoup(p, 'html.parser')
    link = s.find(href=re.compile('download'))
    get_link = link.get('href')
    req_proxy.generate_proxied_request(get_link)
    shorten = Shortener('Tinyurl')
    shrink_url = shorten.short(get_link)

print('Downloading: ' + '(' + artistName + spaceInput + hyphenInput + spaceInput + songName + ')' +
      ' via Short URL => ' + shrink_url + '\n')
file = wget.download(shrink_url, out='/tmp/')
print(file + ' Downloaded!' + '\n')
mp3 = MP3File(file)
mp3.set_version(VERSION_BOTH)
mp3.artist = artistName
mp3.song = songName
mp3.album = 'Telegram'
mp3.save()

audio = open(file, 'rb')
token = 'my_token'
chat_id = '@my_chat'
tb = telebot.TeleBot(token)
tb.config['api_key'] = token
tb.config['chat_id'] = chat_id
tb.config['audio'] = audio
user = tb.get_me()
print(user)

chat_id = '@testing_now'
tb.send_message(chat_id, text='TESTING')

print('Uploading File to Telegram Channel...\n')
tb.send_audio(chat_id, audio)
tb.send_message(chat_id, text, parse_mode="Markdown")
print('File Uploaded!\n')

print("Found: " + artistName + hyphenInput + songName)
print("Downloaded: " + artistName + hyphenInput + songName)
print("Uploaded to: " + chat_id)

