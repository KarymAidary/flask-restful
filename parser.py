import requests
from HTMLParser import HTMLParser


class TegHTMLParser(HTMLParser):
    d = dict()

    def handle_starttag(self, tag, attrs):
        if tag in self.d.keys():
            self.d[tag] += 1
        else:
            self.d[tag] = 1

    def get_el(self, url):
        request = requests.get(url)
        self.feed(request.text)
        return self.d.items()
