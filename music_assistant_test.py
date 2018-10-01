'''
We're going to search for the music(done)
Download track as mp3-file(done)
And upload it to the Telegram channel(done)
Let's Go! :)
12.08.2018 @ 4:03
All done!
09.09.2018 @ 18:09
'''

import re
import wget
import telebot
import requests
from bs4 import BeautifulSoup
from pyshorteners import Shortener
from multiprocessing import Connection

banner = '''
--------------------------------------------------------------------------------------------------
  __  __                 _                                   _         _                     _    
 |  \/  |               (_)              /\                 (_)       | |                   | |   
 | \  / |  _   _   ___   _    ___       /  \     ___   ___   _   ___  | |_    __ _   _ __   | |_  
 | |\/| | | | | | / __| | |  / __|     / /\ \   / __| / __| | | / __| | __|  / _` | | '_ \  | __| 
 | |  | | | |_| | \__ \ | | | (__     / ____ \  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_  
 |_|  |_|  \__,_| |___/ |_|  \___|   /_/    \_\ |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__| 
         FOR TELEGRAM             v.1.01b          by Viacheslav Vorotilin aka "music meister"      
--------------------------------------------------------------------------------------------------
'''
print(banner + "\n")

artistName = input('Artist: ')  # Variable for Artist Name
songName = input('Name: ')  # Variable for Song Name
mixName = input('Mix Name: ')  # Variable for Remix Name
blankInput = str()  # String Variable for Blank Input

'''
plusInput = '+'                     # Variable for a Plus [+]
underInput = '_'                    # Variable for an Underscore [_]
'''

spaceInput = ' '  # Variable for a Space [ ]
hyphenInput = '-'  # Variable for a Hyphen [-]
codeOpen = '<code>'  # Variable for Text-Formatting
codeClose = '</code>'  # Variable for Text-Formatting
boldOpen = '<b>'  # Variable for Text-Formatting
boldClose = '</b>'  # Variable for Text-Formatting

if mixName == blankInput:
    query = (artistName + spaceInput + songName)
elif songName == blankInput:
    query = (artistName + spaceInput + mixName)
elif artistName == blankInput:
    query = (songName + spaceInput + mixName)
else:
    query = (artistName + spaceInput + songName + spaceInput + mixName)
print(query + "\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) \
    Gecko/20100101 Firefox/45.0'
}

url = 'https://mp3cc.biz/search/f/' + query + '/'

with open('parse.txt', "wb") as lf:
    try:
        response = requests.get(url, headers=headers, stream=True)
        lf.write(response.content)
        lf.close()
    except ConnectionError as e:
        raise Connection

with open('parse.txt', "r", encoding='UTF-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    link = soup.find(href=re.compile("download"))
    file = link.get('href')
    print("Long URL => " + file + "\n")


class shrinkApp(Shortener):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shortener = Shortener('Tinyurl')
        self.url = str(file)
        self.shrinkUrl = self.shortener.short(self.url)

        print("Downloading File via Short URL => " + self.shrinkUrl + "\n")
        mp3 = wget.download(self.shrinkUrl, out='/tmp/')
        print('File Downloaded!' + "\n")

        token = '658217975:AAFIqRoLhfS7x4XpCNHoPGsqttQp_QFsPU0'
        tb = telebot.TeleBot(token)
        chat_id = '@testing_now'

        audio = open(mp3, 'rb')
        print('Uploading File to Telegram Channel...' + "\n")
        tb.send_audio(chat_id, audio)
        print('File Uploaded!' + "\n")

        tb.send_message(chat_id, text=text, parse_mode='HTML')

        if mixName == blankInput:
            text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + codeClose)
        else:
            text = {
                codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName \
                + spaceInput + '(' + mixName + ')' + codeClose
            }


app = shrinkApp()
