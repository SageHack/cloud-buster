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
    type=str
)

args = parser.parse_args()
buster = CloudBuster(args.target)

if args.check_ip:
    buster.check_ip(args.check_ip)
elif args.target:
    buster.scan_main()
    if buster.protected():
        buster.scan_subdomains()
        buster.scan_panels()
        buster.search_crimeflare()
    buster.print_infos()
else:
    parser.print_help()
