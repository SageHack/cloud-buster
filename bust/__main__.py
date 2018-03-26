from buster import CloudBuster
from cli import args, parser
from options import Options
import os.path
import sys

logo = """
============ The =====,---/V\\
==== CloudBUSTER ====~|__(o.o)
=== by @SageHack =====UU  UU
"""


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
        if technique is 'subdomain':
            found = sub_scan_subdomain(buster, args)
        else:
            found = sub_scan(buster, args, technique)

        if found:
            return

    match_not_found(buster)


def match_not_found(buster):
    buster.scan_summary()
    print(
        '>> UNABLE TO CONFIRM [%s;interesting ips (%d)] <<' % (
            buster.target['main'].domain,
            len(buster.list_interesting_hosts()),
        ), flush=True
    )


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
        return true


def sub_scan(buster, args, technique):
    scan_technique = getattr(buster, 'scan_'+technique)
    target_found = scan_technique()
    if target_found:
        print_match(buster.target['main'], target_found, technique)
        return True


def scan_list(args):
    file = args.target
    for target in open(file).read().splitlines():
        args.target = target
        print('====================================', flush=True)
        scan(args)


def print_match(target_main, target_found, method):
    print(
        '>> MATCH [%s;%s;%s;%s;%s;%s] <<' % (
            target_main.domain,
            method,
            target_found.domain
            if target_found.domain != target_found.ip
            else target_main.domain,
            target_found.ip,
            target_found.status,
            target_found.reason,
        ), flush=True
    )


def main(args):
    print(logo)
    if not args.target:
        parser.print_help()
    if os.path.isfile(args.target):
        scan_list(args)
    else:
        scan(args)


try:
    main(args)
except KeyboardInterrupt:
    print('>> INTERRUPTED BY USER <<')
    sys.exit()
