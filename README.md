# Music Downloader & Uploader to Telegram

## Overview

This project is designed to search for music tracks, download them as MP3 files, and upload them to a Telegram channel. The process is automated and uses various libraries for web scraping, downloading, and interacting with Telegram.

### Features
- Search for music tracks.
- Download tracks as MP3 files.
- Upload MP3 files to a specified Telegram channel.

### Changelog
- **12.08.2018 @ 4:03** - Project start.
- **09.09.2018 @ 18:09** - All tasks done!

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Required Python libraries (listed below)

### Required Libraries

Install the required libraries using `pip`:
```sh
pip install os re wget telebot requests beautifulsoup4 pyshorteners mp3-tagger http-request-randomizer
```

## Usage

### Input Data
The script will prompt for the following inputs:
- Artist Name
- Song Name
- Remixed by (optional)

### Running the Script
To run the script, execute the following command:
```sh
python main.py
```

### Example Input
```
Artist: The Beatles
Name: Hey Jude
Remixed by: 
```

### Workflow

1. **Input Information**: Enter the artist name, song name, and optionally, the remixer's name.
2. **Search and Download**: The script searches for the track, downloads it, and renames it.
3. **Edit MP3 Tags**: It updates the MP3 tags with the provided information.
4. **Upload to Telegram**: The MP3 file is uploaded to the specified Telegram channel.

## Code Explanation

### Import Libraries
```python
import os
import re
import wget
import telebot
import requests
from bs4 import BeautifulSoup
from pyshorteners import Shortener
from mp3_tagger import MP3File, VERSION_BOTH
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
```

### Banner
A banner is printed at the start of the script.
```python
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
```

### User Input
```python
artistName = input('Artist: ')     
songName = input('Name: ')        
mixName = input('Remixed by: ')   
blankInput = str()                  
```

### Query Construction
```python
if mixName == blankInput:
    query = (artistName + spaceInput + songName)
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName + codeClose)
    newName = ('/tmp/' + artistName + hyphenInput + songName + '.mp3')
else:
    query = (artistName + spaceInput + songName + spaceInput + mixName)
    text = (codeOpen + artistName + spaceInput + hyphenInput + spaceInput + songName
            + '(' + mixName + ')' + codeClose)
    newName = ('/tmp/' + artistName + hyphenInput + songName + hyphenInput + mixName + '.mp3')
print('\nQuery: ' + query)
```

### Download and Process
The script fetches the download link, shortens it, downloads the file, and updates the ID3 tags.
```python
# Proxy Setup and URL Request
req_proxy = RequestProxy()
url = 'https://mp3cc.biz/search/f/' + query + '/'

while not req_proxy.generate_proxied_request(url):
    print('\nNext proxy for Base URL')
else:
    print('\nConnected to Base URL!')
    pass

# Save Response to File
with open('parse.txt', 'wb') as f:
    response = requests.get(url)
    f.write(response.content)

# Parse Download Link
with open('parse.txt', 'r', encoding='UTF-8') as p:
    s = BeautifulSoup(p, 'html.parser')
    link = s.find(href=re.compile('download'))
    get_link = link.get('href')

# Shorten URL
access_token = 'my_bitly_token'
tinyurl_short = Shortener('Tinyurl')
bitly_short = Shortener('Bitly', bitly_token=access_token)

while not req_proxy.generate_proxied_request(get_link):
    print('\nNext proxy for Parsed URL')
else:
    print('\nConnected to Parsed URL!')
    pass

shrink_url = bitly_short.short(get_link)
if shrink_url:
    print('\nBitLy: ' + str(shrink_url))
else:
    shrink_url = tinyurl_short.short(get_link)
    print('\nTinyurl: ' + str(shrink_url))

# Download File
while not req_proxy.generate_proxied_request(shrink_url):
    print('\nNext proxy for Shrink URL')
else:
    print('\nConnected to Shrink URL!')
    pass

print('\nDownloading: ' + query + ' via Short URL --> ' + shrink_url)
file = wget.download(shrink_url, out='/tmp')
print('\nDownloaded!: ' + str(file))

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
```

### Upload to Telegram
```python
# Rename and Open File
print('\nFilename will be: ' + newName)
os.rename(str(file), newName)
audio = open(newName, 'rb')
token = 'my_bot_token'
chat_id = '@my_chat_id'
tb = telebot.TeleBot(token)
tb_status = str(tb.get_me())
print('\nStatus: ' + tb_status)

# Upload to Telegram
print('\nUploading File to a Telegram Channel: ' + chat_id)
print('\nMessage will be: ' + str(text))
send = tb.send_audio(chat_id, audio)
message_id = send.message_id
caption = str(text)
tb.edit_message_caption(caption, chat_id, message_id, parse_mode='HTML')
print('\nFile Uploaded!')
```

### Status Imprint
```python
print('\nFound: ' + query)
print('\nDownloaded: ' + query)
print('\nUploaded to: ' + chat_id)
```

## License
This project is licensed under the MIT License.

## Author
Viacheslav Vorotilin aka "Music Meister"
