import urllib.request
from urllib.error import HTTPError
import re
import ssl


class PageTitle(object):

    opened = {}

    def __init__(self, url, host=None):
        self.url = url
        self.host = host

        if host:
            self.id = self.url+':'+self.host
        else:
            self.id = self.url

    def __get__(self, obj=None, objtype=None):
        if self.id in self.opened:
            return self.opened[self.id].title

        request = urllib.request.Request(url=self.url, headers=self.headers)

        try:
            opened = urllib.request.urlopen(
                request,
                timeout=10,
                context=self.context
            )
            html = opened.read()
        except (OSError, HTTPError):
            opened = None
            html = None

        title = self.parse_title(html)
        self.opened[self.id] = opened
        return title

    def __set__(self, obj=None, val=None):
        raise AttributeError

    @property
    def context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    @property
    def headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)' +
            'Gecko/200101 Firefox/36.0'
        }
        if self.host:
            headers['Host'] = self.host
        return headers

    def parse_title(self, html):
        html = str(html)
        get_title = re.compile(
            '<title>(.*?)</title>',
            re.IGNORECASE | re.DOTALL
        )
        search_result = get_title.search(html)

        if search_result:
            return search_result.group(1)
        else:
            return None
