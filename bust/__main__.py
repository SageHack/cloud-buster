from buster import CloudBuster
from cli import args, parser

buster = CloudBuster(args.target)

if args.target:
    buster.scan_main()
    if buster.protected():
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

        buster.print_infos()
else:
    parser.print_help()
