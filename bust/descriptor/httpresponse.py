import http.client


class HttpResponse(object):

    def __init__(self, domain, timeout=10, ssl=False):
        self.domain = domain
        self.timeout = timeout
        self.ssl = ssl
        self.response = None

    def __get__(self):
        if self.response:
            return self.response

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
        except:
            self.response = None
            return self.response

        response = connection.getresponse()
        connection.close()

        self.response = response
        return self.response

    def __set__(self):
        raise AttributeError
