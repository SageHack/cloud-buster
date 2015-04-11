from detect import Detector
from target import Target
from panels import PANELS
import re


class CloudBuster:

    def __init__(self, domain):
        self.domain = domain
        self.targets = {
            'main': None,
            'subdomains': [],
            'panels': [],
            'mxs': []
        }
        self.crimeflare_ip = None

    def check_ip(self, ip):
        detector = Detector()
        cf_owned = detector.in_range(ip)
        print(cf_owned)

    def scan_main(self):
        target = Target(
            domain=self.domain,
            name='Target'
        )
        target.scan()
        target.print_infos()
        self.targets['main'] = target

    def protected(self):
        if not self.targets['main'] or type(self.targets['main']) != Target:
            return False

        return self.targets['main'].protected()

    def scan_subdomains(self, subdomains=None):
        subs = [sub for sub in open('lists/subdomains').read().splitlines()]

        if subdomains:
            for sub2scan in subdomains:
                if sub2scan not in subs:
                    subs.append(sub2scan)

        for sub in subs:
            if not subdomains or sub in subdomains:
                subdomain = sub+'.'+self.domain
                target = Target(
                    domain=subdomain,
                    name='Subdomain'
                )
                target.scan()
                target.print_infos()
                self.targets['subdomains'].append(target)

    def scan_panels(self, panels=None):

        for panel in PANELS:
            if not panels or panel['name'] in panels:
                target = Target(
                    domain=self.domain+':'+str(panel['port']),
                    name='Pannel ('+panel['name']+')',
                    timeout=2,
                    ssl=panel['ssl']

                )
                target.scan()
                target.print_infos()
                self.targets['panels'].append(target)

    def search_crimeflare(self):
        for line in open('lists/ipout'):
            if self.domain in line:
                self.crimeflare_ip = line.partition(' ')[2].rstrip()
                return

    def scan_mx_records(self):
        try:
            import dns.resolver
        except:
            from errors import DNSPythonError
            DNSPythonError.output()
            return

        mxs = dns.resolver.query(self.domain, 'MX')
        mx_priority = re.compile('\d* ')

        for mx in mxs:
            hostname = mx_priority.sub('', mx.to_text()[:-1])
            target = Target(
                domain=hostname,
                name='MX',
                timeout=1
            )
            target.scan()
            target.print_infos()
            self.targets['mxs'].append(target)

    def print_infos(self):
        print('== SCAN SUMARY ==')

        if self.targets['main']:
            print('Target: '+self.targets['main'].host['domain'])
            print('> ip: '+self.targets['main'].host['ip'])
            print('> protected: '+str(self.targets['main'].protected()))

        print('== Found ips ==')

        for host in self.list_interesting_hosts():
            print(host['ip']+' ('+host['domain']+')')

    def list_interesting_hosts(self):
        hosts = []
        targets = self.targets['subdomains'] \
            + self.targets['panels'] \
            + self.targets['mxs']

        for target in targets:
            if target.host['ip'] and not target.protected():
                hosts.append({
                    'ip': target.host['ip'],
                    'domain': target.host['domain']
                })

        if self.crimeflare_ip:
            hosts.append({
                'ip': self.crimeflare_ip,
                'domain': 'from crimeflare.com db'
            })

        return hosts
