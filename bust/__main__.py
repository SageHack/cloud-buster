from buster import CloudBuster
from cli import args, parser
from options import Options
import os.path
import sys

logo = """
\033[31m============ The =====\033[35m,---\033[37m/V\\
\033[32m==== CloudBUSTER ====\033[37m~\033[35m|  \033[37m(o.o)
\033[34m=== by @SageHack =====\033[37muu\033[35m--\033[37muu\033[0m
"""


def main(args):
    print(logo, flush=True)
    if not args.target:
        parser.print_help()
    if os.path.isfile(args.target):
        scan_list(args)
    else:
        scan(args)


def scan_list(args):
    file = args.target
    for target in open(file).read().splitlines():
        args.target = target
        print('====================================', flush=True)
        scan(args)


def scan(args):
    buster = CloudBuster(args.target)
    buster.scan_main()

    if not buster.resolving():
        print('>> CANT RESOLVE HOST <<', flush=True)
        return

    if not buster.protected():
        print('>> NOT BEHIND CLOUDFLARE <<', flush=True)
        if not Options.SCAN_ANYWAY:
            return

    for technique in args.scan:
        if technique == 'subdomain':
            found = sub_scan_subdomain(buster, args)
        else:
            found = sub_scan(buster, args, technique)

        if found:
            return

    match_not_found(buster)


def sub_scan(buster, args, technique):
    scan_technique = getattr(buster, 'scan_'+technique)
    target_found = scan_technique()
    if target_found:
        print_match(buster.target['main'], target_found, technique)
        return True


def sub_scan_subdomain(buster, args):
    dept = {
        'simple': int(30),
        'normal': int(100),
        'full': None
    }

    target_found = buster.scan_subdomain(
        args.sub if args.sub else None,
        dept[args.dept]
    )

    if target_found:
        print_match(buster.target['main'], target_found, 'subdomain')
        return True


def print_match(target_main, target_found, method):
    print(
        '>> MATCH [%s;%s;%s;%s] <<' % (
            target_main.domain,
            method,
            target_found.domain
            if target_found.domain != target_found.ip
            else target_main.domain,
            target_found.ip,
        ), flush=True
    )


def match_not_found(buster):
    buster.scan_summary()
    print(
        '>> UNABLE TO CONFIRM [%s;interesting ips (%d)] <<' % (
            buster.target['main'].domain,
            len(buster.list_interesting_hosts()),
        ), flush=True
    )


try:
    main(args)
except KeyboardInterrupt:
    print('>> INTERRUPTED BY USER <<', flush=True)
    sys.exit()
