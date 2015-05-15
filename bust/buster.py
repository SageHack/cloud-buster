from cloudflarenetwork import CloudFlareNetwork
from descriptor.mxrecords import MxRecords
from descriptor.pagetitle import PageTitle
from target import Target
from panels import PANELS


class CloudBuster:

    def __init__(self, domain):
        self.domain = domain
        self.targets = {
            'main': None,
            'subdomains': [],
            'panels': [],
            'mxs': [],
            'crimeflare': []
        }
        self.crimeflare_ip = None

    def resolving(self):
        if self.targets['main']:
            if self.targets['main'].ip:
                return True

        return False

    def check_ip(self, ip):
        net = CloudFlareNetwork()
        print(net.in_range(ip))

    def scan_main(self):
        target = Target(self.domain, 'target')
        target.print_infos()
        self.targets['main'] = target

    def protected(self):
        if not self.targets['main'] or type(self.targets['main']) != Target:
            return False

        return self.targets['main'].protected

    def scan_subdomains(self, subdomains=None):
        if subdomains:
            toscan = subdomains
        else:
            toscan = open('lists/subdomains').read().splitlines()

        subTargets = [
            Target(sub+'.'+self.domain, 'subdomain', timeout=5)
            for sub in toscan
        ]

        for target in subTargets:
            target.print_infos()
            if self.is_interesting(target):
                self.targets['subdomains'].append(target)
                if self.match(target):
                    print('>> MATCH <<')
                    return target

        return None

    def scan_panels(self, panels=None):
        panTargets = []

        for panel in PANELS:
            if not panels or panel['name'] in panels:
                target = Target(
                    domain=self.domain,
                    name=panel['name']+':'+str(panel['port']),
                    port=panel['port'],
                    timeout=2,
                    ssl=panel['ssl']
                )
                panTargets.append(target)

        for target in panTargets:
            target.print_infos()
            if self.is_interesting(target):
                self.targets['panels'].append(target)
                if self.match(target):
                    print('>> MATCH <<')
                    return target

        return None

    def search_crimeflare(self):
        cfTargets = []

        for line in open('lists/ipout'):
            if self.domain in line:
                crimeflare_ip = line.partition(' ')[2].rstrip()
                target = Target(crimeflare_ip, 'crimeflare')
                cfTargets.append(target)

        for target in cfTargets:
            target.print_infos()
            if self.is_interesting(target):
                self.targets['crimeflare'].append(target)
                if self.match(target):
                    print('>> MATCH <<')
                    return target

        return None

    def scan_mx_records(self):

        mxs = MxRecords(self.domain).__get__()
        if not mxs:
            return

        mxTargets = [
            Target(mx, 'mx', timeout=1)
            for mx in mxs
        ]

        for target in mxTargets:
            target.print_infos()
            if self.is_interesting(target):
                self.targets['mxs'].append(target)
                if self.match(target):
                    print('>> MATCH <<')
                    return target
        return None


    def is_interesting(self, target):
        return target.ip and target.protected is False

    def match(self, possible_target):
        main_target = self.targets['main']
        main_target.title = PageTitle(
            'http://'+main_target.domain
        ).__get__()
        possible_target.title = PageTitle(
            'http://'+possible_target.ip,
            main_target.domain
        ).__get__()
        return main_target.title == possible_target.title

    def scan_summary(self):
        print('[SCAN SUMMARY]')

        if self.targets['main']:
            print('Target: '+self.targets['main'].domain)
            print('> ip: '+str(self.targets['main'].ip))
            print('> protected: '+str(self.targets['main'].protected))

        print('[found ips]')

        for host in self.list_interesting_hosts():
            print(host['ip']+' > '+host['description'])

        target_title = PageTitle(
            'http://'+self.targets['main'].domain
        ).__get__()

        if target_title:
            prev_ip = None

            for host in self.list_interesting_hosts():
                if prev_ip != host['ip']:
                    prev_ip = host['ip']

                    title = PageTitle(
                        'http://'+host['ip'],
                        self.targets['main'].domain
                    ).__get__()

                    if title == target_title:
                        print('>> CONFIRMED <<')
                        print('> ip: '+host['ip'])
                        print('> title: '+str(title))
                        return

        print('>> UNABLE TO CONFIRM <<')

    def list_interesting_hosts(self):
        hosts = []
        targets = self.targets['subdomains'] \
            + self.targets['panels'] \
            + self.targets['mxs'] \
            + self.targets['crimeflare']

        for target in targets:
            if target.ip and not target.protected \
                    and target.status and target.status != 400:
                hosts.append({
                    'ip': target.ip,
                    'description': target.domain+' / '+target.name
                })

        return hosts
