from cloudflarenetwork import CloudFlareNetwork
from descriptor.mxrecords import MxRecords
from target import Target
from panels import PANELS


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
        net = CloudFlareNetwork()
        print(net.in_range(ip))

    def scan_main(self):
        target = Target(
            name='Target',
            domain=self.domain
        )
        target.print_infos()
        self.targets['main'] = target

    def protected(self):
        if not self.targets['main'] or type(self.targets['main']) != Target:
            return False

        return self.targets['main'].protected

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
                    name='Subdomain',
                    domain=subdomain,
                    timeout=5
                )
                target.print_infos()
                self.targets['subdomains'].append(target)

    def scan_panels(self, panels=None):

        for panel in PANELS:
            if not panels or panel['name'] in panels:
                target = Target(
                    name='Pannel ('+panel['name']+')',
                    domain=self.domain,
                    port=panel['port'],
                    timeout=2,
                    ssl=panel['ssl']

                )
                target.print_infos()
                self.targets['panels'].append(target)

    def search_crimeflare(self):
        for line in open('lists/ipout'):
            if self.domain in line:
                self.crimeflare_ip = line.partition(' ')[2].rstrip()
                return

    def scan_mx_records(self):

        for mx in MxRecords(self.domain).__get__():
            target = Target(
                name='MX',
                domain=mx,
                timeout=1
            )
            target.print_infos()
            self.targets['mxs'].append(target)

    def print_infos(self):
        print('== SCAN SUMARY ==')

        if self.targets['main']:
            print('Target: '+self.targets['main'].domain)
            print('> ip: '+str(self.targets['main'].ip))
            print('> protected: '+str(self.targets['main'].protected))

        print('== Found ips ==')

        for host in self.list_interesting_hosts():
            print(host['ip']+' > '+host['description'])

    def list_interesting_hosts(self):
        hosts = []
        targets = self.targets['subdomains'] \
            + self.targets['panels'] \
            + self.targets['mxs']

        for target in targets:
            if target.ip and not target.protected \
                    and target.status and target.status != 400:
                hosts.append({
                    'ip': target.ip,
                    'description': target.domain+' / '+target.name
                })

        if self.crimeflare_ip:
            hosts.append({
                'ip': self.crimeflare_ip,
                'description': 'from crimeflare.com db'
            })

        return hosts
