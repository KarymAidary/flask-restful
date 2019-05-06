from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    d = dict()

    def handle_starttag(self, tag, attrs):
        if tag in self.d.keys():
            self.d[tag] += 1
        else:
            self.d[tag] = 1
