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
import time
import wget
import telebot
from bs4 import BeautifulSoup
from pyshorteners import Shortener
from requests import request
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError
from requests.packages.urllib3 import HTTPConnectionPool
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

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

if __name__ == '__main__':

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

    start = time.time()
    req_proxy = RequestProxy()
    print("Initialization took: {0} sec".format((time.time() - start)))
    print("Size: {0}".format(len(req_proxy.get_proxy_list())))
    print("ALL = {0} ".format(list(map(lambda x: x.get_address(), req_proxy.get_proxy_list()))))

    url = 'https://mp3cc.biz/search/f/' + query + '/'

    with open('parse.txt', 'wb') as f:
        request = req_proxy.generate_proxied_request(url)
        f.write(request.content)

        print("Proxies Request Took: {0} sec => Status: {1}".format((time.time() - start), request.__str__()))
        print("-> Going to sleep..")
        time.sleep(10)

    with open('parse.txt', 'r', encoding='UTF-8') as p:
        s = BeautifulSoup(p, 'html.parser')
        link = s.find(href=re.compile('download'))
        get_link = link.get('href')

        try:
            shorten = Shortener('Tinyurl')
            shrink_url = shorten.short(get_link)
        except ReadTimeout as e:
            raise ReadTimeout(e, request=request)
        else:
            pass

    print('Downloading: ' + '(' + artistName + spaceInput + hyphenInput + spaceInput + songName + ')' +
          ' via Short URL => ' + shrink_url + '\n')
    file = req_proxy.generate_proxied_request(shrink_url)
    f = wget.download(file, out='/tmp/')
    print(file + ' Downloaded!' + '\n')

    mp3 = MP3File(file)
    art = mp3.artist
    sng = mp3.song
    alb = mp3.album
    mp3.set_version(VERSION_BOTH)
    mp3.artist = artistName
    mp3.song = songName
    mp3.album = 'Telegram'
    mp3.save()
    chat_id = '@testing_now'
    token = '658217975:AAEmtIoL3SX-Cf8budKCQHpd99BDNlEMnRg'
    tb = telebot.TeleBot(token)
    user = tb.get_me()
    print(user)

    with open(file, 'rb') as audio:
        print('Uploading File to Telegram Channel...\n')
        tb.send_audio(chat_id, audio)
        print('File Uploaded!\n')
        tb.send_message(chat_id, text)
        print("Found: " + artistName + hyphenInput + songName)
        print("Downloaded: " + artistName + hyphenInput + songName)
        print("Uploaded to: " + chat_id)

import cleaner
