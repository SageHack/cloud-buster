from os import linesep
from cloudflarenetwork import CloudFlareNetwork
from descriptor.mxrecords import MxRecords
from options import Options
from target import Target
from DNSDumpsterAPI import DNSDumpsterAPI
from matchengine import MatchEngine
import re


class CloudBuster:

    def __init__(self, domain):
        self.domain = domain
        self.target = {
            'main': None,
            'other': []
        }

    def resolving(self):
        if self.target['main']:
            if self.target['main'].ip:
                return True

        return False

    def check_ip(self, ip):
        net = CloudFlareNetwork()
        print(net.in_range(ip), flush=True)

    def scan_main(self):
        target = Target(self.domain, 'target')
        target.print_infos()
        self.target['main'] = target

    def protected(self):
        if not self.target['main'] or type(self.target['main']) != Target:
            return False

        return self.target['main'].protected

    def scan_subdomain(self, subdomains=None, dept=None):
        if subdomains:
            toscan = subdomains
        else:
            toscan = open('lists/subdomains').read().splitlines()
            if dept:
                del toscan[dept:]

        targets = [
            Target(sub+'.'+self.domain, 'subdomain', timeout=5)
            for sub in toscan
        ]

        return self.scan(targets)

    def scan_crimeflare(self):
        global cfdb
        targets = []

        """load cfdb in memory for __main__.scan_list()"""
        if 'cfdb' not in globals():
            cfdb = [
                i for i
                in open('crimeflare/db').readlines()
            ]

        for line in cfdb:
            if self.domain in line:
                ip = line.partition(' ')[2].rstrip()
                targets.append(Target(ip, 'crimeflare'))

        return self.scan(targets)

    def scan_dnsdumpster(self):
        try:
            results = DNSDumpsterAPI().search(self.domain)
            records = results['dns_records']
        except IndexError:
            results = None
            records = []

        if 'host' in records:
            ips = []
            domains = []

            for host in records['host']:
                if not host['provider'].startswith('Cloudflare'):
                    ips.append(host['ip'])
                    """For some reason Dumpster API return <br in domains"""
                    domains.append(re.sub('<br', '', host['domain']))

            targets = [
                Target(host, 'dnsdumpster', timeout=5)
                for host in set(domains + ips)
            ]
            return self.scan(targets)

    def scan_mx(self):
        mxs = MxRecords(self.domain).__get__()
        if mxs:
            targets = [
                Target(mx, 'mx', timeout=5)
                for mx in mxs
            ]
            return self.scan(targets)

    def scan(self, targets):
        for target in targets:
            target.print_infos()
            if self.is_interesting(target):
                self.target['other'].append(target)
                if self.match(target):
                    return target
        return None

    def is_interesting(self, target):
        return target.ip and not target.protected

    def match(self, possible_origin):

        if Options.SCAN_EVERYTHING:
            return False

        return MatchEngine.is_origin(
            self.target['main'].domain,
            possible_origin.ip
        )

    def scan_summary(self):
        print('[SCAN SUMMARY]', flush=True)

        if self.target['main']:
            print(
                'Target: '+self.target['main'].domain+linesep
                + '> ip: '+str(self.target['main'].ip)+linesep
                + '> protected: '+str(self.target['main'].protected),
                flush=True
            )

        print('[interesting ips]', flush=True)

        for host in self.list_interesting_hosts():
            print(host['ip']+' > '+host['description'], flush=True)

    def list_interesting_hosts(self):
        hosts = []
        targets = self.target['other']

        for target in targets:
            if self.is_interesting(target) \
                    and target.status and target.status != 400:
                hosts.append({
                    'ip': target.ip,
                    'description': target.domain+' / '+target.name
                })

        return hosts
