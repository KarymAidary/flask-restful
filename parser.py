from HTMLParser import HTMLParser


class TegHTMLParser(HTMLParser):
    d = dict()

    def handle_starttag(self, tag, attrs):
        if tag in self.d.keys():
            self.d[tag] += 1
        else:
            self.d[tag] = 1

    def get_el(self, req):
        self.feed(req.text)
        return self.d.items()
