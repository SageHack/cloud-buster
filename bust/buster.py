from detect import Detector
from target import Target
from panels import PANELS


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
        for panel in PANELS:
            target = Target(
                self.domain+':'+str(panel['port'])
            )
            target.option('name', 'Pannel ('+panel['name']+')')
            target.option('timeout', 1)
            target.option('ssl', panel['ssl'])
            target.scan()
            target.infos()
            self.targets['panels'].append(target)
