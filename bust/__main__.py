import argparse
from buster import CloudBuster

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

buster = CloudBuster(args.target)

if args.check_ip:
    buster.check_ip(args.check_ip)
elif args.target:
    buster.target()
    if buster.target_on_cloudflare():
        buster.scan_subdomains()
        if args.panels or args.panels == []:
            buster.scan_panels(args.panels)
else:
    parser.print_help()
