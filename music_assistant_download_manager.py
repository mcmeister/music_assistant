## Music Assistant Download Manager

import requests
from lxml import html


class Proxy(object):
    proxy_url = 'https://free-proxy-list.net/'
    proxi_list = []

    def __init__(self):
        r = requests.get(self.proxy_url)
        str = html.fromstring(r.content)
        result = str.xpath("//th[@class='hm']/td[1]/text()")
        self.proxi_list = result

    def get_proxy(self):
        for proxy in self.proxi_list:
            url = 'http://' + proxy
            try:
                r = requests.get('http://ya.ru', proxies={'http': url})
                if r.status_code == 200:
                    return url
            except requests.exceptions.ConnectionError:
                continue

proxy = Proxy()
proxy = proxy.get_proxy()
print(proxy)
r = requests.get('http://speed-tester.info/check_ip.php', proxies={'http': proxy})
print(r.content)