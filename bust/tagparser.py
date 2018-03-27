from html.parser import HTMLParser


class TagParser(HTMLParser):
    def __init__(self, tags):
        HTMLParser.__init__(self)
        self.match = False
        self.tag = {tag: None for tag in tags}

    def handle_starttag(self, tag, attributes):
        self.match = False
        if tag in self.tag:
            self.match = tag

    def handle_data(self, data):
        if self.match:
            self.tag[self.match] = data
            self.match = False
