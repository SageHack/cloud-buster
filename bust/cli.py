import argparse

parser = argparse.ArgumentParser(
    description='Default behavior is check mx records,' +
    'subdomains and crimeflare database.'
)

parser.add_argument(
    'target',
    metavar='DOMAIN',
    type=str,
    help='Domain name or file with name list, one per line'
)

scan_choices = 'mx, crimeflare, dnsdumpster, subdomains'
parser.add_argument(
    '--scan',
    metavar='OPTION',
    nargs='*',
    choices=scan_choices.split(', '),
    default='mx crimeflare dnsdumpster subdomains',
    help=scan_choices
)

parser.add_argument(
    '--sub',
    metavar='SUBDOMAIN',
    nargs='*',
    help='Scan specified subdomains'
)

parser.add_argument(
    '--dept',
    metavar='DEPT',
    choices=['simple', 'normal', 'full'],
    default='simple',
    help='[simple] scan top 30 subdomains, \
    [normal] top 200, \
    [full] scan over 9000 subs!!!'
)

args = parser.parse_args()
