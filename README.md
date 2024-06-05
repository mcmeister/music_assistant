# Music Downloader & Uploader to Telegram

## Overview
This project is designed to search for music tracks, download them as MP3 files, and upload them to a Telegram channel. The process is automated and utilizes various libraries for web scraping, downloading, and interacting with Telegram.

## Features
- Search for music tracks.
- Download tracks as MP3 files.
- Upload MP3 files to a specified Telegram channel.

## Changelog
- **12.08.2018 @ 4:03** - Project start.
- **09.09.2018 @ 18:09** - All tasks done!

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required Python libraries (listed below)

### Required Libraries
Install the required libraries using pip:
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
To run the script on a PC, execute:
```sh
python main.py
```
For the mobile version, the process is similar, but ensure the correct file paths are used as per the mobile script.

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
The script starts by importing necessary libraries for file operations, web requests, web scraping, MP3 tagging, URL shortening, and Telegram bot interaction.

### Banner
A banner is printed at the start of the script to display project information.

### User Input
The script prompts the user to input the artist name, song name, and optionally, the remixer's name.

### Query Construction
The script constructs a search query based on the user input and prepares the filename for the downloaded MP3 file.

### Download and Process
The script:
- Sets up a proxy for web requests.
- Searches for the music track.
- Parses the download link from the search results.
- Shortens the URL for downloading.
- Downloads the MP3 file.
- Updates the MP3 tags with the provided information.

### Upload to Telegram
The script:
- Renames the downloaded file.
- Uploads the MP3 file to the specified Telegram channel.
- Edits the message caption with the formatted track information.

### Status Imprint
The script prints the status of the search, download, and upload processes.

## Mobile Version
The mobile version of the script functions similarly but uses file paths suitable for a mobile environment. Ensure to update paths and necessary configurations accordingly.

## License
This project is licensed under the MIT License.

## Author
Viacheslav Vorotilin aka "Music Meister"
