from descriptor.httpresponse import HttpResponse
from descriptor.hostbyname import HostByName
from cloudflarenetwork import CloudFlareNetwork


class Target:

    def __init__(self, domain, name=None, port=None, timeout=10, ssl=False):
        self.domain = domain
        if name:
            self.name = name
        else:
            self.name = domain
        self.port = port
        self.timeout = timeout
        self.ssl = ssl

    @property
    def ip(self):
        return HostByName(self.domain).__get__()

    @property
    def response(self):
        return HttpResponse(
            self.domain, self.port, self.timeout, self.ssl
        ).__get__()

    @property
    def cloudflare_ip(self):
        net = CloudFlareNetwork()
        return net.in_range(self.ip)

    @property
    def cloudflare_ray(self):
        try:
            return self.response.getheader('CF-RAY')
        except (OSError, ConnectionError, AttributeError):
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
        except (OSError, ConnectionError, AttributeError, TypeError):
            return None

    @property
    def status(self):
        try:
            return self.response.status
        except (OSError, ConnectionError, AttributeError):
            return None

    @property
    def reason(self):
        try:
            return self.response.reason
        except (OSError, ConnectionError, AttributeError):
            return None

    @property
    def protected(self):
        return bool(self.cloudflare_ip) or bool(self.cloudflare_ray)

    def print_infos(self):
        print('['+self.name+'] '+self.domain, flush=True)
        if not self.ip or self.status is None:
            return

        print(
            '* ip: %s (CF %s%s)' % (
                self.ip,
                'yes' if self.cloudflare_ip else 'no',
                ' RAY-'+self.cloudflare_ray if self.cloudflare_ray else ''
            ), flush=True
        )

        if self.enabled:
            print(
                '* http: %s %s %s' % (
                    self.enabled+' -' if self.enabled else '',
                    self.status,
                    self.reason if self.reason else ''
                ), flush=True
            )
        else:
            print(
                '* status: %s %s' % (self.status, self.reason),
                flush=True
            )
