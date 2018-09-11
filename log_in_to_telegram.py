## Message Bot for Telegram Channel

import requests

token = '658217975:AAGpMceHLVj7M3PyJHXEMqIeqSDWzeT1E24'
id = '@mc_meister'
text = 'Halleluya!'

url = 'https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+id+'&text='+text
r = requests.post(url)