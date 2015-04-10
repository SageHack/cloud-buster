import http.client
import socket
from detect import Detector


class Target:

    def __init__(self, domain):
        self.info = {
            'name': None,
        }

        self.host = {
            'domain': domain,
            'ip': None,
            'cf-ip': None,
        }

        self.http = {
            'response': None,
            'status': None,
            'enabled': None,
            'cf-ray': None,
        }

        self.options = {
            'name': 'Host',
            'timeout': 10,
            'ssl': False
        }

    def scan(self):
        self.ip(self.host['domain'])
        if not self.host['ip']:
            return None
        self.http_response(self.host['domain'])

    def option(self, option, value=None):
        if value:
            self.options[option] = value
        else:
            return self.options[option]

    def protected(self):
        return bool(self.http['cf-ray'])

    def print_infos(self):
        print(self.options['name']+': '+self.host['domain'])
        if not self.host['ip']:
            print('> not-found')
            return

        print('> ip: '+self.host['ip'])
        print('> cf-ip: '+str(self.host['cf-ip']))
        print('> cf-ray: '+str(self.http['cf-ray']))
        print('> http: '+str(self.http['enabled']))
        print('> status: '+str(self.http['status']))

    def ip(self, domain):
        try:
            host_ip = socket.gethostbyname(domain)
        except:
            return

        d = Detector()
        self.host['ip'] = host_ip
        self.host['cf-ip'] = d.in_range(host_ip)

    def http_response(self, domain):
        try:
            if self.options['ssl']:
                connection = http.client.HTTPSConnection(
                    domain, timeout=self.options['timeout']
                )
            else:
                connection = http.client.HTTPConnection(
                    domain, timeout=self.options['timeout']
                )
            connection.request('HEAD', '/')
            response = connection.getresponse()
            connection.close()
        except:
            return

        self.http['response'] = response

        if response:
            self.http['cf-ray'] = response.getheader('CF-RAY')
            self.http['enabled'] = \
                response.getheader('Server')
            if response.getheader('X-Powered-By'):
                self.http['enabled'] = self.http['enabled'] \
                    + ' ' \
                    + response.getheader('X-Powered-By')
            self.http['status'] = \
                str(response.status)+' '+response.reason
        else:
            self.http['cf-ray'] = None
            self.http['enabled'] = False
