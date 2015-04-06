from detect import Detector
from target import Target
from panels import PANELS


class CloudBuster:

    def __init__(self, domain):
        self.domain = domain
        self.targets = {
            'main': None,
            'subdomains': [],
            'panels': []
        }

    def check_ip(self, ip):
        detector = Detector()
        cf_owned = detector.in_range(ip)
        print(cf_owned)

    def scan_main(self):
        target = Target(self.domain)
        target.option('name', 'Target')
        target.scan()
        target.print_infos()
        self.targets['main'] = target

    def on_cloudflare(self):
        if not self.targets['main'] or type(self.targets['main']) != Target:
            return False

        return self.targets['main'].on_cloudflare()

    def scan_subdomains(self):
        subs = [sub for sub in open('lists/subdomains').read().splitlines()]
        for sub in subs:
            subdomain = sub+'.'+self.domain
            target = Target(subdomain)
            target.option('name', 'Subdomain')
            target.scan()
            target.print_infos()
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
            target.print_infos()
            self.targets['panels'].append(target)

    def print_infos(self):
        print('=== SCAN SUMARY ===')
        print('Target: '+self.targets['main'].host['domain'])
        print('> ip: '+self.targets['main'].host['ip'])
        print('> on CloudFlare: '+str(self.targets['main'].on_cloudflare()))
        print('== Found ips ==')
        for ip in self.list_interesting_ips():
            print(ip)

    def list_interesting_ips(self):
        ips = []
        targets = self.targets['subdomains'] + self.targets['panels']

        for target in targets:
            ip = target.host['ip']
            if ip and not target.on_cloudflare():
                if ip not in ips:
                    ips.append(ip)

        return ips
