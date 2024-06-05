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

# Banner
banner = '''
--------------------------------------------------------------------------------------------------
  __  __                 _                                   _         _                     _    
 |  \/  |               (_)              /\                 (_)       | |                   | |   
 | \  / |  _   _   ___   _    ___       /  \     ___   ___   _   ___  | |_    __ _   _ __   | |_  
 | |\/| | | | | | / __| | |  / __|     / /\ \   / __| / __| | | / __| | __|  / _` | | '_ \  | __| 
 | |  | | | |_| | \__ \ | | | (__     / ____ \  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_  
 |_|  |_|  \__,_| |___/ |_|  \___|   /_/    \_\ |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__| 
         FOR TELEGRAM           v.1.01b         by Viacheslav Vorotilin aka "Music Meister"      
--------------------------------------------------------------------------------------------------
'''
print(banner)

# User Input
artist_name = input('Artist: ')
song_name = input('Name: ')
mix_name = input('Remixed by: ')
blank_input = str()

# Constants
SPACE = ' '
HYPHEN = '-'
CODE_OPEN = '<code>'
CODE_CLOSE = '</code>'
BOLD_OPEN = '<b>'
BOLD_CLOSE = '</b>'

# Generate Query
if mix_name == blank_input:
    query = f"{artist_name} {song_name}"
    text = f"{CODE_OPEN}{artist_name} - {song_name}{CODE_CLOSE}"
    new_name = f"/tmp/{artist_name}-{song_name}.mp3"
else:
    query = f"{artist_name} {song_name} {mix_name}"
    text = f"{CODE_OPEN}{artist_name} - {song_name} ({mix_name}){CODE_CLOSE}"
    new_name = f"/tmp/{artist_name}-{song_name}-{mix_name}.mp3"
logging.info(f"Query: {query}")

# Base URL
url = f"https://mp3cc.biz/search/f/{query}/"

# Proxy Request
req_proxy = RequestProxy()
response = None

while not response:
    try:
        response = req_proxy.generate_proxied_request(url)
        logging.info('Connected to Base URL!')
    except Exception as e:
        logging.error(f"Failed to connect, retrying... Error: {e}")

# Save to File
with open('parse.txt', 'wb') as f:
    response = requests.get(url)
    f.write(response.content)

# Parse from File
with open('parse.txt', 'r', encoding='UTF-8') as p:
    soup = BeautifulSoup(p, 'html.parser')
    link = soup.find(href=re.compile('download'))
    get_link = link.get('href')

# Shorten URL
access_token = 'my_bitly_token'
tinyurl_short = Shortener('Tinyurl')
bitly_short = Shortener('Bitly', bitly_token=access_token)

shrink_url = None
response = None

while not response:
    try:
        response = req_proxy.generate_proxied_request(get_link)
        logging.info('Connected to Parsed URL!')
    except Exception as e:
        logging.error(f"Failed to connect, retrying... Error: {e}")

try:
    shrink_url = bitly_short.short(get_link)
    logging.info(f'BitLy: {shrink_url}')
except Exception as e:
    logging.error(f"BitLy failed, trying TinyURL... Error: {e}")
    shrink_url = tinyurl_short.short(get_link)
    logging.info(f'TinyURL: {shrink_url}')

# Download File
response = None

while not response:
    try:
        response = req_proxy.generate_proxied_request(shrink_url)
        logging.info('Connected to Shrink URL!')
    except Exception as e:
        logging.error(f"Failed to connect, retrying... Error: {e}")

logging.info(f'Downloading: {query} via Short URL --> {shrink_url}')
file = wget.download(shrink_url, out='/tmp')
logging.info(f'Downloaded: {file}')

# Edit ID3 Tags
mp3 = MP3File(file)
mp3.set_version(VERSION_BOTH)
mp3.artist = artist_name
mp3.song = song_name
mp3.album = 'Telegram'
mp3.publisher = ''
mp3.save()
tags = mp3.get_tags()
logging.info(tags)

# Telegram Bot
logging.info(f'Filename will be: {new_name}')
os.rename(file, new_name)
audio = open(new_name, 'rb')
token = 'my_bot_token'
chat_id = '@my_chat_id'
tb = telebot.TeleBot(token)
tb_status = tb.get_me()
logging.info(f'Status: {tb_status}')

# Upload File
logging.info(f'Uploading File to Telegram Channel: {chat_id}')
logging.info(f'Message will be: {text}')
send = tb.send_audio(chat_id, audio)
message_id = send.message_id
caption = text
tb.edit_message_caption(caption, chat_id, message_id, parse_mode='HTML')
logging.info('File Uploaded!')

# Status Imprint
logging.info(f'Found: {query}')
logging.info(f'Downloaded: {query}')
logging.info(f'Uploaded to: {chat_id}')

import cleaner
