import http.client
import socket
from detect import Detector


class Target:

    def __init__(self, domain):
        self.domain = domain
        self.ip = self.ip(domain)
        self.http_response = self.http_response(domain)

    def infos(self):
        print('Target: '+self.domain)

        if self.ip:
            print('> ip: '+self.ip)

            d = Detector()
            print ('> cf-ip: '+str(d.in_range(self.ip)))

        ray = self.http_response.getheader('CF-RAY')
        if ray:
            print ('> cf-ray: '+ray)

    def ip(self, domain):
        try:
            return socket.gethostbyname(domain)
        except:
            print('Error: Cannot find ip for '+domain)
            return

    def http_response(self, domain):
        connection = http.client.HTTPConnection(domain)
        try:
            connection.request("HEAD", "/")
        except:
            print('Error: Connect via HTTP to '+domain)
            return
        reponse = connection.getresponse()
        connection.close()
        return reponse
