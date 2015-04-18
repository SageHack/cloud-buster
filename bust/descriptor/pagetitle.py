import urllib.request
import re


class PageTitle(object):

    titles = {}

    def __init__(self, address, host_header=None):
        self.address = address
        self.host_header = host_header

    def __get__(self, obj=None, objtype=None):
        if self.address in self.titles:
            print('title already in memory')
            return self.titles[self.address]

        print('fetching page title')
        try:
            html = urllib.request.urlopen(self.address).read()
        except:
            html = None

        html = str(html)
        get_title = re.compile(
            '<title>(.*?)</title>',
            re.IGNORECASE | re.DOTALL
        )
        search_result = get_title.search(html)

        if search_result:
            title = search_result.group(1)
        else:
            title = None

        self.titles[self.address] = title
        return title
