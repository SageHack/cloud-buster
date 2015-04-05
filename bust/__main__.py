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
    target.infos()
    if target.on_cloudflare():
        scan_subdomains(domain)


def scan_subdomains(domain):
    subs = [sub for sub in open('lists/subdomains').read().splitlines()]
    for sub in subs:
        subdomain = sub+'.'+domain
        target = Target(subdomain)
        target.infos()


if args.check_ip:
    check_ip(args.check_ip)
elif args.target:
    target(args.target)
else:
    parser.print_help()
