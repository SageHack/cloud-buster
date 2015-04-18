import http.client


class HttpResponse(object):

    responses = {}

    def __init__(self, domain, timeout=10, ssl=False):
        self.domain = domain
        self.timeout = timeout
        self.ssl = ssl

    def __get__(self, obj=None, objtype=None):
        if self.domain in self.responses:
            return self.responses[self.domain]

        if self.ssl:
            connection = http.client.HTTPSConnection(
                self.domain, timeout=self.timeout
            )
        else:
            connection = http.client.HTTPConnection(
                self.domain, timeout=self.timeout
            )

        try:
            connection.request('HEAD', '/')
            response = connection.getresponse()
        except:
            response = None

        connection.close()

        self.responses[self.domain] = response
        return response

    def __set__(self, obj=None, val=None):
        raise AttributeError
