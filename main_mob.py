"""
We're going to search for the music (done)
Download track as mp3-file (done)
And upload it to Telegram channel (done)
Let's Go! :)
12.08.2018 @ 4:03
All done!
09.09.2018 @ 18:09
"""

# Import Input

import os
import re
import wget
import telebot
import requests
from bs4 import BeautifulSoup
from pyshorteners import Shortener
from mp3_tagger import MP3File, VERSION_BOTH
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Banner Input

banner = '''
---------------------------------------------------------
MUSIC ASSISTANT FOR TELEGRAM
v.1.01b
by Viacheslav Vorotilin
aka "music meister"      
---------------------------------------------------------
'''
print(banner)

# User Input

artistName = input('Artist: ')      # Variable for Artist Name
songName = input('Name: ')          # Variable for Song Name
mixName = input('Remixed by: ')     # Variable for DJ Name
blankInput = str()                  # String Variable for Blank Input

# Program Input

spaceInput = ' '                    # Variable for a Space [ ]
hyphenInput = '-'                   # Variable for a Hyphen [-]
codeOpen = '<code>'                 # Variable for Text-Formatting
codeClose = '</code>'               # Variable for Text-Formatting

# Cute Queries

if mixName == blankInput:
    query = f"{artistName}{spaceInput}{songName}"
    text = f"{codeOpen}{artistName}{spaceInput}{hyphenInput}{spaceInput}{songName}{codeClose}"
    newName = f"/storage/emulated/0/temp/{artistName}{hyphenInput}{songName}.mp3"
else:
    query = f"{artistName}{spaceInput}{songName}{spaceInput}{mixName}"
    text = f"{codeOpen}{artistName}{spaceInput}{hyphenInput}{spaceInput}{songName}({mixName} Remix){codeClose}"
    newName = f"/storage/emulated/0/temp/{artistName}{hyphenInput}{songName}{hyphenInput}{mixName}.mp3"

print(f'\nWorking on Request: {query}')

# Base URL

url = f'https://mp3cc.biz/search/f/{query}/'

# Proxy Headers Request

req_proxy = RequestProxy()

while not req_proxy.generate_proxied_request(url):
    print('\nNext proxy for "Base URL"')
else:
    print('\nConnected to "Base URL!"')

# Save To File

with open('parse.txt', 'wb') as f:
    response = requests.get(url)
    f.write(response.content)

# Parse From File

with open('parse.txt', 'r', encoding='UTF-8') as p:
    s = BeautifulSoup(p, 'html.parser')
    link = s.find(href=re.compile('download'))
    get_link = link.get('href')

# Shrink Parsed URL

access_token = 'my_bitly_token'
tinyurl_short = Shortener('Tinyurl')
bitly_short = Shortener('Bitly', bitly_token=access_token)

try:
    shrink_url = bitly_short.short(get_link)
except requests.exceptions.Timeout as ert:
    print("Timeout Error:", ert)
    pass

try:
    shrink_url = tinyurl_short.short(get_link)
except requests.exceptions.Timeout as ert:
    print("Timeout Error:", ert)
    pass

# Download Shrink URL

while not req_proxy.generate_proxied_request(shrink_url):
    print('\nNext proxy for "Shrink URL"')
else:
    print('\nConnected to "Shrink URL!"')

print(f'\nDownloading: {query} via Short URL --> {shrink_url}')
file = wget.download(shrink_url, out='/tmp')
print(f'\nDownloaded: {file}')

# Edit ID3 Tags

mp3 = MP3File(file)
mp3.set_version(VERSION_BOTH)
mp3.artist = artistName
mp3.song = songName
mp3.album = 'Telegram'
mp3.publisher = ''
mp3.save()
tags = mp3.get_tags()
print(tags)

# Telegram Bot

print(f'\nNew Filename is: {newName}')
os.rename(str(file), newName)
audio = open(newName, 'rb')
token = 'my_bot_token'
chat_id = '@my_chat_id'
tb = telebot.TeleBot(token)
tb_status = str(tb.get_me())
print(f'\nStatus: {tb_status}')

# Upload File

print(f'\nUploading File to Telegram Channel: {chat_id}')
print(f'\nThe Caption is: {text}')
send = tb.send_audio(chat_id, audio)
message_id = send.message_id
caption = str(text)
tb.edit_message_caption(caption, chat_id, message_id, parse_mode='HTML')
print('\nFile Uploaded!')

# Status Imprint

print(f'\nFound: {query}')
print(f'Downloaded: {query}')
print(f'Uploaded to: {chat_id}')

import cleaner_mob
