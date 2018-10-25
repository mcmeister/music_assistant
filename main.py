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
import lxml.html
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
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + codeClose)
    newName = ('/tmp/' + artistName + hyphenInput + songName + '.mp3')
else:
    query = (artistName + spaceInput + songName + spaceInput + mixName)
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName
            + '(' + mixName + ')' + codeClose)
    newName = ('/tmp/' + artistName + hyphenInput + songName + hyphenInput + mixName + '.mp3')

print('\nWorking on Request: ' + query)    

# baseURL

url = 'https://mp3cc.biz/search/f/' + query + '/'

# proxy_headersRequest

req_proxy = RequestProxy()

while not req_proxy.generate_proxied_request(url):
    print('\nNext proxy for "Base URL"')
else:
    print('\nConnected to "Base URL!"')
    response = requests.get(url)

page = response.content
dom = lxml.html.fromstring(page)

links = dom.xpath('//div[@class="playlist-btn"]//a/@href')
for link in links:
    print(link)

    while not req_proxy.generate_proxied_request(link):
        print('\nNext proxy for "Parsed URL"')
    else:
        print('\nConnected to Parsed "URL!"')
        pass

    print('\nDownloading: ' + query + '\n')
    file = wget.download(link, out='/tmp')
    print('\nDownloaded: ' + format(file))

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

    print('\nNew Filename is: ' + newName)
    os.rename(str(file), newName)
    audio = open(newName, 'rb')
    token = 'my_bot_token'
    chat_id = '@my_chat_id'
    tb = telebot.TeleBot(token)
    tb_status = str(tb.get_me())
    print('\nTeleBot Status: ' + tb_status)

# uploadFile

    print('\nUploading File to Telegram Channel: ' + chat_id)
    print('\nThe Caption is: ' + str(text))
    send = tb.send_audio(chat_id, audio)
    message_id = send.message_id
    caption = str(text)
    tb.edit_message_caption(caption, chat_id, message_id, parse_mode='HTML')
    print('\nFile Uploaded!')

# statusImprint

    print('\nFound: ' + query)
    print('Downloaded: ' + file)
    print('Uploaded to: ' + chat_id)

    import cleaner
