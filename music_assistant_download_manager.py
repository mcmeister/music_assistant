## Music Assistant Download Manager

from bs4 import BeautifulSoup, SoupStrainer

with open('test.txt', 'r') as f:
    for link in BeautifulSoup(f.read(), parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            print(link['href'])