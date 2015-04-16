from descriptor.httpresponse import HttpResponse
from descriptor.hostbyname import HostByName
from cloudflarenetwork import CloudFlareNetwork


class Target:

    def __init__(self, domain, name='Host', timeout=10, ssl=False):
        self.domain = domain
        self.name = name
        self.ip = HostByName(domain).__get__()
        if self.ip:
            self.response = HttpResponse(domain, timeout, ssl).__get__()

    @property
    def cloudflare_ip(self):
        net = CloudFlareNetwork()
        return net.in_range(self.ip)

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

    def print_infos(self):
        print(self.name+': '+self.domain)
        if not self.ip:
            print('> not-found')
            return

        print('> ip: '+str(self.ip))
        print('> CF-ip: '+str(self.cloudflare_ip))
        print('> CF-ray: '+str(self.cloudflare_ray))
        print('> http: '+str(self.enabled))
        print('> status: '+str(self.status))
