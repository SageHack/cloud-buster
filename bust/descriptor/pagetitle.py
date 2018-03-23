import urllib.request
from urllib.error import HTTPError
from ipurlredirecthandler import IpUrlRedirectHandler
import re
import ssl


class PageTitle(object):

    titles = {}

    def __init__(self, url, host=None):
        self.url = url
        self.host = host

        if host:
            self.id = self.host+'@'+self.url
        else:
            self.id = self.url

    def __get__(self, obj=None, objtype=None):
        if self.id in self.titles:
            return self.titles[self.id]

        urllib.request.install_opener(self.opener)
        request = urllib.request.Request(url=self.url, headers=self.headers)
        print('> reading: '+self.id)

        try:
            opened = urllib.request.urlopen(
                request,
                timeout=10
            )
            html = opened.read()
            title = self.parse_title(html)
        except (OSError, HTTPError):
            opened = None
            html = None
            title = None

        self.titles[self.id] = title
        return title

    def __set__(self, obj=None, val=None):
        raise AttributeError

    @property
    def headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)' +
            'Gecko/200101 Firefox/36.0'
        }
        if self.host:
            headers['Host'] = self.host
        return headers

    @property
    def opener(self):
        handles = []

        """Override redirect handler"""
        handles.append(IpUrlRedirectHandler())

        """Disable SSL cert verification"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handles.append(urllib.request.HTTPSHandler(context=ctx))
        
        opener = urllib.request.build_opener(*handles)

        return opener

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
