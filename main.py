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
from pyshorteners import Shortener
from requests.packages.urllib3 import HTTPConnectionPool
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

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

# ProxySoon

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) \
    Gecko/20100101 Firefox/45.0'
}

# SomeLink

url = 'https://mp3cc.biz/search/f/' + query + '/'

# MessBegins

with open('parse.txt', 'wb') as lf:
    response = requests.get(url, headers=headers, stream=True)
    lf.write(response.content)
    lf.close()

with open('parse.txt', 'r', encoding='UTF-8') as p:
    s = BeautifulSoup(p, 'html.parser')
    link = s.find(href=re.compile('download'))
    print(type(link))
    get_link = link.get('href')
    
try:
    shorten = Shortener('Tinyurl')
    shrink_url = shorten.short(get_link)
except HTTPConnectionPool(host='tinyurl.com', port=80) as e:
  repeat
else:
  pass

print('Downloading: ' + '(' + artistName + spaceInput + hyphenInput + spaceInput + songName + ')' +
      ' via Short URL => ' + shrink_url + '\n')
    
try:
    mp3 = wget.download(shrink_url, out='/tmp/')
except:
  pass

print(mp3 + ' Downloaded!' + '\n')
    tags = mp3.get_tags()
    del tags
    mp3.set_version(VERSION_BOTH)
    mp3.artist = artistName
    mp3.song = songName
    mp3.album = mixName
    mp3.save()
    chat_id = '@my_id'
    token = 'my_token'
    tb = telebot.TeleBot(token)
    user = tb.get_me()
print(user)
    audio = open(mp3, 'rb')
print('Uploading File to Telegram Channel...\n')

try:
    tb.send_audio(chat_id, audio)
except:
  pass

print('File Uploaded!\n')
    tb.send_message(chat_id, text)
print("Found: " + artistName + hyphenInput + songName)
print("Downloaded: " + artistName + hyphenInput + songName)
print("Uploaded to: " + chat_id)

#MessCleans

import cleaner
