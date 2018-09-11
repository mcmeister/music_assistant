'''
We're going to search for the music(done)
Download track as mp3-file(done)
And upload it to Telegram channel(done)
Let's Go! :)
12.08.2018 @ 4:03
All done!
09.09.2018 @ 18:09
'''

## Banner Section

banner = '''
--------------------------------------------------------------------------------------------------
  __  __                 _                                   _         _                     _    
 |  \/  |               (_)              /\                 (_)       | |                   | |   
 | \  / |  _   _   ___   _    ___       /  \     ___   ___   _   ___  | |_    __ _   _ __   | |_  
 | |\/| | | | | | / __| | |  / __|     / /\ \   / __| / __| | | / __| | __|  / _` | | '_ \  | __| 
 | |  | | | |_| | \__ \ | | | (__     / ____ \  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_  
 |_|  |_|  \__,_| |___/ |_|  \___|   /_/    \_\ |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__| 
                                                                                                                                                                                                 
--------------------------------------------------------------------------------------------------
'''
print(banner)

import re
import wget
import telebot
import requests
from bs4 import BeautifulSoup
from pyshorteners import Shortener

## User Input Section

artistName = input('Artist: ')                  ## Variable for Artist Name
songName = input('Name: ')                      ## Variable for Song Name
mixName = input('Mix Name: ')                   ## Variable for Remix Version
blankInt = str()                                ## String Variable for Blank Input

## Programm Input Section

'''
plusInt = '+'                                   ## Variable for a Plus [+]
underInt = '_'                                  ## Variable for an Underscore [_]
'''

spaceInt = ' '                                  ## Variable for a Space [ ]
hyphenInt = '-'                                 ## Variable for a Hyphen [-]
codeOpen = '<code>'                             ## Variable for Text-Formatting
codeClose = '</code>'                           ## Variable for Text-Formatting
boldOpen = '<b>'                                ## Variable for Text-Formatting
boldClose = '</b>'                              ## Variable for Text-Formatting

## Appropriate to Website's Search Query (Including or Excluding Remix Version)

if mixName == blankInt:
    query = (artistName + spaceInt + songName)
elif songName == blankInt:
    query = (artistName + spaceInt + mixName)
elif artistName == blankInt:
    query = (songName + spaceInt + mixName)
else:
    query = (artistName + spaceInt + songName + spaceInt + mixName)
print(query + "\n")

## Headers to Access Website

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; \
    Intel Mac OS X 10.9; \
    rv:45.0) Gecko/20100101 Firefox/45.0'
}

## Appropriate URL-String to Access Website's Search

url = 'https://mp3cc.biz/search/f/' + query + '/'

## Save Search Results to Text-File

with open('parse.txt', "wb") as lf:
    response = requests.get(url, headers=headers, stream=True)
    lf.write(response.content)
    lf.close()

## Parse Mp3-Link from Text-File

with open('parse.txt', "r", encoding='UTF-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    link = soup.find(href=re.compile("download"))
    file = link.get('href')
    print("Long URL => " + file + "\n")
    print(len(file))

## shrinkApp - URL-Shortener Section

class shrinkApp(Shortener):
    def __init__(self):
        self.option = int(1)
        self.url = str(file)
        self.shortener = Shortener('Tinyurl')

        if self.option == 1:
            self.shrinkTheUrl()
        else:
            pass

    def shrinkTheUrl(self):
        self.shrinkUrl = self.shortener.short(self.url)
        print("Downloading File via Short URL => " + self.shrinkUrl + "\n")

## Download Mp3-File with Tinyurl

        mp3 = wget.download(self.shrinkUrl, out='/temp/')
        print('File Downloaded!' + "\n")

## Telegram Bot Section

        TOKEN = 'MY_TOKEN'
        tb = telebot.TeleBot(TOKEN)
        chat_id = '@my_channel'
        audio = open(mp3, 'rb')

## Send audio file to Telegram Channel

        tb.send_message(chat_id, text='<i>Uploading Audio...</i>', parse_mode='HTML')
        print('Uploading File to Telegram Channel...' + "\n")

        tb.send_audio(chat_id, audio)

        tb.send_message(chat_id, text='<b>Upload Completed!</b>', parse_mode='HTML')
        print('File Uploaded!' + "\n")

## Send message to Telegram Channel

        tb.send_message(chat_id, text=text, parse_mode='HTML')

if mixName == blankInt:
    text = (codeOpen + artistName + spaceInt + hyphenInt + spaceInt + songName + codeClose)
else:
    text = {
    codeOpen + artistName + spaceInt + hyphenInt + spaceInt + songName \
    + spaceInt + '(' + mixName + ')' + codeClose
}

app = shrinkApp()

import delete_mp3