import argparse
from detect import Detector
from target import Target

parser = argparse.ArgumentParser(
    description='CloudFlare pentest tool'
)
parser.add_argument(
    '-i',
    '--check_ip',
    metavar='IP',
    type=str,
    help='Check if an IPv4/6 is owned by CloudFlare'
)
parser.add_argument(
    '-t',
    '--target',
    metavar='DOMAIN',
    type=str,
    help='Scan website for information'
)
args = parser.parse_args()


def check_ip(ip):
    detector = Detector()
    cf_owned = detector.in_range(ip)
    print(cf_owned)


def target(domain):
    target = Target(domain)
    target.option('name', 'Target')
    target.scan()
    target.infos()
    if target.on_cloudflare():
        scan_subdomains(domain)
        scan_panels(domain)


def scan_subdomains(domain):
    subs = [sub for sub in open('lists/subdomains').read().splitlines()]
    for sub in subs:
        subdomain = sub+'.'+domain
        target = Target(subdomain)
        target.option('name', 'Subdomain')
        target.scan()
        target.infos()


def scan_panels(domain):
    # http://www.mysql-apache-php.com/ports.htm
    panels = [
        {'name': 'cpanel', 'port': 2082, 'ssl': False},
        {'name': 'cpanel-ssl', 'port': 2083, 'ssl': True},
        {'name': 'whm', 'port': 2086, 'ssl': False},
        {'name': 'whm-ssl', 'port': 2087, 'ssl': True},
        {'name': 'cpmail', 'port': 2095, 'ssl': False},
        {'name': 'cpmail-ssl', 'port': 2096, 'ssl': True},
        {'name': 'plesk', 'port': 8087, 'ssl': False},
        {'name': 'plesk-ssl', 'port': 8443, 'ssl': True},
    ]

    for panel in panels:
        target = Target(
            domain+':'+str(panel['port'])
        )
        target.option('name', 'Admin ('+panel['name']+')')
        target.option('timeout', 1)
        target.option('ssl', panel['ssl'])
        target.scan()
        target.infos()


if args.check_ip:
    check_ip(args.check_ip)
elif args.target:
    target(args.target)
else:
    parser.print_help()
