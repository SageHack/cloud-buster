import http.client
import socket
from detect import Detector


class Target:

    def __init__(self, domain):
        self.domain = domain
        self.ip = self.ip(domain)
        if not self.ip:
            return None
        self.http_response = self.http_response(domain)
        if not self.http_response:
            self.cf_ray = None
        else:
            self.cf_ray = self.http_response.getheader('CF-RAY')

    def infos(self):
        print('Target: '+self.domain)
        if not self.ip:
            print('> not-found')
        else:
            print('> ip: '+self.ip)
            d = Detector()
            print ('> cf-ip: '+str(d.in_range(self.ip)))
            print ('> cf-ray: '+str(self.cf_ray))

    def ip(self, domain):
        try:
            return socket.gethostbyname(domain)
        except:
            return

    def http_response(self, domain):
        connection = http.client.HTTPConnection(domain)
        try:
            connection.request("HEAD", "/")
        except:
            return
        reponse = connection.getresponse()
        connection.close()
        return reponse
