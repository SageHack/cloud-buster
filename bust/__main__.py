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
    help='Main target'
)
parser.add_argument(
    '--panels',
    nargs='*',
    help='Scan popular panel services',
    choices=(
        'cpanel',
        'cpanel-ssl',
        'whm',
        'whm-ssl',
        'plesk',
        'plesk-ssl'
    )
)
args = parser.parse_args()


def check_ip(ip):
    detector = Detector()
    cf_owned = detector.in_range(ip)
    print(cf_owned)


def target(domain, args):
    target = Target(domain)
    target.option('name', 'Target')
    target.scan()
    target.infos()
    if target.on_cloudflare():
        scan_subdomains(domain)
        if args.panels or args.panels == []:
            scan_panels(domain, args)


def scan_subdomains(domain):
    subs = [sub for sub in open('lists/subdomains').read().splitlines()]
    for sub in subs:
        subdomain = sub+'.'+domain
        target = Target(subdomain)
        target.option('name', 'Subdomain')
        target.scan()
        target.infos()


def scan_panels(domain, args):
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
        if args.panels == [] or panel['name'] in args.panels:
            target = Target(
                domain+':'+str(panel['port'])
            )
            target.option('name', 'Pannel ('+panel['name']+')')
            target.option('timeout', 1)
            target.option('ssl', panel['ssl'])
            target.scan()
            target.infos()


if args.check_ip:
    check_ip(args.check_ip)
elif args.target:
    target(args.target, args)
else:
    parser.print_help()
