import urllib.request
import http.client
from urllib.error import HTTPError
from ipurlredirecthandler import IpUrlRedirectHandler
from tagparser import TagParser
import re
import ssl
import random


class RequestContent(object):

    content = {}

    def __init__(self, url, host=None):
        self.url = url
        self.host = host

        if host:
            self.id = self.host+'@'+self.url
        else:
            self.id = self.url

    def __get__(self, obj=None, objtype=None):
        id = self.id

        if id in self.content:
            return self.content[id]

        self.content[id] = self.get_content()

        return self.content[id]

    def __set__(self, obj=None, val=None):
        raise AttributeError

    @property
    def headers(self):
        global uagent
        headers = {}

        if self.host:
            headers['Host'] = self.host

        if 'uagent' not in globals():
            uagent = random.choice(open('lists/uagents').read().splitlines())

        headers['User-Agent'] = uagent

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

    def get_content(self):
        content = {
            'status': None,
            'title': None,
            'html': None
        }

        urllib.request.install_opener(self.opener)
        request = urllib.request.Request(url=self.url, headers=self.headers)
        print('* reading: '+self.id, flush=True)

        try:
            opened = urllib.request.urlopen(
                request,
                timeout=10
            )
            html = opened.read()
        except (OSError, HTTPError, http.client.BadStatusLine):
            return content

        content['status'] = str(opened.status)+' '+opened.reason

        if not html:
            return content

        content['html'] = str(html)

        parser = TagParser(['title'])
        parser.feed(content['html'])
        content['title'] = parser.tag['title']

        return content
