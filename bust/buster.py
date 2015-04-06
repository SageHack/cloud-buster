from detect import Detector
from target import Target


class CloudBuster:

    domain = None
    targets = {
        'main': None,
        'subdomains': [],
        'panels': []
    }

    def __init__(self, domain):
        self.domain = domain

    def check_ip(self, ip):
        detector = Detector()
        cf_owned = detector.in_range(ip)
        print(cf_owned)

    def target(self):
        target = Target(self.domain)
        target.option('name', 'Target')
        target.scan()
        target.infos()
        self.targets['main'] = target

    def target_on_cloudflare(self):
        if not self.targets['main']:
            return False
        if type(self.targets['main']) != Target:
            return False

        return self.targets['main'].on_cloudflare()

    def scan_subdomains(self):
        subs = [sub for sub in open('lists/subdomains').read().splitlines()]
        for sub in subs:
            subdomain = sub+'.'+self.domain
            target = Target(subdomain)
            target.option('name', 'Subdomain')
            target.scan()
            target.infos()
            self.targets['subdomains'].append(target)

    def scan_panels(self):
        # http://www.mysql-apache-php.com/ports.htm
        panels = [
            {'name': 'cpanel', 'port': 2082, 'ssl': False},
            {'name': 'cpanel-ssl', 'port': 2083, 'ssl': True},
            {'name': 'whm', 'port': 2086, 'ssl': False},
            {'name': 'whm-ssl', 'port': 2087, 'ssl': True},
            {'name': 'plesk', 'port': 8087, 'ssl': False},
            {'name': 'plesk-ssl', 'port': 8443, 'ssl': True},
        ]

        for panel in panels:
            target = Target(
                self.domain+':'+str(panel['port'])
            )
            target.option('name', 'Pannel ('+panel['name']+')')
            target.option('timeout', 1)
            target.option('ssl', panel['ssl'])
            target.scan()
            target.infos()
            self.targets['panels'].append(target)
