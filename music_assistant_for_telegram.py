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
         FOR TELEGRAM           v.1.01b         by Vorotilin Viacheslav aka "music meister"      
--------------------------------------------------------------------------------------------------
'''
print(banner)

## Module Section

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
blankInput = str()                              ## String Variable for Blank Input

## Program Input Section

'''
plusInput = '+'                                 ## Variable for a Plus [+]
underInput = '_'                                ## Variable for an Underscore [_]
'''

spaceInput = ' '                                ## Variable for a Space [ ]
hyphenInput = '-'                               ## Variable for a Hyphen [-]
codeOpen = '<code>'                             ## Variable for Text-Formatting
codeClose = '</code>'                           ## Variable for Text-Formatting
boldOpen = '<b>'                                ## Variable for Text-Formatting
boldClose = '</b>'                              ## Variable for Text-Formatting

## Appropriate to Website's Search Query: Including or Excluding Remix Version

if mixName == blankInput:
    query = (artistName + spaceInput + songName)
elif songName == blankInput:
    query = (artistName + spaceInput + mixName)
elif artistName == blankInput:
    query = (songName + spaceInput + mixName)
else:
    query = (artistName + spaceInput + songName + spaceInput + mixName)
print(query + "\n")

## Headers to Access Website

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) \
    Gecko/20100101 Firefox/45.0'
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

## Download Mp3-File with Tinyurl

        print("Downloading File via Short URL => " + self.shrinkUrl + "\n")
        mp3 = wget.download(self.shrinkUrl, out='/temp/')
        print('File Downloaded!' + "\n")

## Telegram Bot Section

        TOKEN = 'MY_TOKEN'
        tb = telebot.TeleBot(TOKEN)
        chat_id = '@my_channel'
        audio = open(mp3, 'rb')

## Send Audio File to Telegram Channel

        tb.send_message(chat_id, text='<i>Uploading New Music...</i>', parse_mode='HTML')
        print('Uploading File to Telegram Channel...' + "\n")

        tb.send_audio(chat_id, audio)

        tb.send_message(chat_id, text='<b>Music Uploaded!</b>', parse_mode='HTML')
        print('File Uploaded!' + "\n")

## Send Message to Telegram Channel

        tb.send_message(chat_id, text=text, parse_mode='HTML')

app = shrinkApp()

## Appropriate Text Message to Post After Upload Completed

if mixName == blankInput:
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + codeClose)
else:
    text = {
    codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName \
    + spaceInput + '(' + mixName + ')' + codeClose
}

## Delete Downloaded Mp3-File

import delete_mp3
