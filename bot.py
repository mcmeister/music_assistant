from pyshorteners import Shortener

class shrinkApp(Shortener):
    def __init__(self):
        banner = '''

         ____  _          _       _    
        / ___|| |__  _ __(_)_ __ | | __
        \___ \| '_ \| '__| | '_ \| |/ /
         ___) | | | | |  | | | | |   < 
        |____/|_| |_|_|  |_|_| |_|_|\_\

        '''
        print(banner)
        self.option = int(input("Option => "))
        self.url = str(input("Enter the URL => "))
        self.shortener = Shortener('Tinyurl')

        if self.option == 1:
            self.shrinkTheUrl()

        elif self.option == 2:
            self.decodeTheUrl()

        else:
            pass

    def shrinkTheUrl(self):
        self.shrinkUrl = self.shortener.short(self.url)
        print("Short URL => " + self.shrinkUrl + "\n")

    def decodeTheUrl(self):
        self.decodedUrl = self.shortener.expand(self.url)
        print("Decoded URL => " + self.decodedUrl + "\n")

app = shrinkApp()