from buster import CloudBuster
from cli import args, parser
import os.path


def scan(args):
    buster = CloudBuster(args.target)
    buster.scan_main()

    if 'subdomains' in args.scan:
        if args.sub:
            buster.scan_subdomains(args.sub)
        else:
            buster.scan_subdomains()

    if 'panels' in args.scan:
        if args.pan:
            buster.scan_panels(args.pan)
        else:
            buster.scan_panels()

    if 'crimeflare' in args.scan:
        buster.search_crimeflare()

    if 'mx' in args.scan:
        buster.scan_mx_records()

    buster.print_infos()


def scan_list(args):
    file = args.target
    for target in open(file).read().splitlines():
        args.target = target
        print('====================================')
        scan(args)


def main(args):
    if not args.target:
        parser.print_help()
    if os.path.isfile(args.target):
        scan_list(args)
    else:
        scan(args)


main(args)
