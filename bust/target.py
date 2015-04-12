import http.client
import socket
from detect import Detector


class Target:

    def __init__(self, domain, name='Host', timeout=10, ssl=False):

        self.domain = domain
        self.name = name
        self.timeout = timeout
        self.ssl = ssl

    @property
    def cloudflare_ip(self):
        d = Detector()
        return d.in_range(self.ip)

    @property
    def cloudflare_ray(self):
        try:
            return self.response.getheader('CF-RAY')
        except:
            return None

    @property
    def enabled(self):
        try:
            if self.response.getheader('X-Powered-By'):
                return self.response.getheader('Server') \
                    + ' ' \
                    + self.response.getheader('X-Powered-By')
            else:
                return self.response.getheader('Server')
        except:
            return None

    @property
    def status(self):
        try:
            return str(self.response.status)+' '+self.response.reason
        except:
            return None

    @property
    def protected(self):
        return bool(self.cloudflare_ray)

    @property
    def ip(self):
        try:
            return self._ip
        except:
            try:
                self._ip = socket.gethostbyname(self.domain)
            except:
                self._ip = None

            return self._ip

    @property
    def response(self):
        try:
            return self._response
        except:
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
                self._response = None
                return self._response

            response = connection.getresponse()
            connection.close()

            self._response = response
            return self._response

    def print_infos(self):
        print(self.name+': '+self.domain)
        if not self.ip:
            print('> not-found')
            return

        print('> ip: '+self.ip)
        print('> CF-ip: '+str(self.cloudflare_ip))
        print('> CF-ray: '+str(self.cloudflare_ray))
        print('> http: '+str(self.enabled))
        print('> status: '+str(self.status))
