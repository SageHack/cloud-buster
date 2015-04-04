import argparse
from cf_detect import CF_Detect

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
args = parser.parse_args()


def check_ip(ip):
    detector = CF_Detect()
    cf_owned = detector.in_range(ip)
    print(cf_owned)


if args.check_ip:
    check_ip(args.check_ip)
else:
    parser.print_help()
