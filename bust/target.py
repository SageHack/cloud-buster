import http.client
import socket
from detect import Detector


class Target:

    def __init__(self, domain, name='Host', timeout=10, ssl=False):

        self.domain = domain
        self.ip = None
        self.cloudflare_ip = None

        self.response = None
        self.status = None
        self.enabled = False
        self.cloudflare_ray = None

        self.name = name
        self.timeout = timeout
        self.ssl = ssl

    def scan(self):
        self.resolve_ip(self.domain)
        if not self.ip:
            return None
        self.http_response(self.domain)

    def protected(self):
        return bool(self.cloudflare_ray)

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

    def resolve_ip(self, domain):
        try:
            host_ip = socket.gethostbyname(domain)
        except:
            return

        d = Detector()
        self.ip = host_ip
        self.cloudflare_ip = d.in_range(host_ip)

    def http_response(self, domain):
        if self.ssl:
            connection = http.client.HTTPSConnection(
                domain, timeout=self.timeout
            )
        else:
            connection = http.client.HTTPConnection(
                domain, timeout=self.timeout
            )
        try:
            connection.request('HEAD', '/')
        except:
            return

        response = connection.getresponse()
        connection.close()

        self.response = response

        if response:
            self.cloudflare_ray = response.getheader('CF-RAY')
            self.enabled = response.getheader('Server')
            self.status = str(response.status)+' '+response.reason
            if response.getheader('X-Powered-By'):
                self.enabled = self.enabled \
                    + ' ' \
                    + response.getheader('X-Powered-By')
