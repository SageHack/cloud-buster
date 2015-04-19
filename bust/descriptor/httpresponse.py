import http.client


class HttpResponse(object):

    responses = {}

    def __init__(self, domain, port=None, timeout=5, ssl=False):
        self.domain = domain
        self.timeout = timeout
        self.ssl = ssl

        if port is None and ssl is False:
            self.port = 80
        elif port is None and ssl is True:
            self.port = 443
        else:
            self.port = port

    @property
    def id(self):
        return self.domain+':'+str(self.port)+(':ssl' if self.ssl else '')

    def __get__(self, obj=None, objtype=None):
        if self.id in self.responses:
            return self.responses[self.id]

        if self.ssl:
            connection = http.client.HTTPSConnection(
                self.domain,
                port=self.port,
                timeout=self.timeout
            )
        else:
            connection = http.client.HTTPConnection(
                self.domain,
                port=self.port,
                timeout=self.timeout
            )

        try:
            connection.request('HEAD', '/')
            response = connection.getresponse()
        except:
            response = None

        connection.close()

        self.responses[self.id] = response
        return response

    def __set__(self, obj=None, val=None):
        raise AttributeError
