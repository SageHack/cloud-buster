import argparse

parser = argparse.ArgumentParser(
    description='Default behavior is scan everything.'
    + ' you can change that by specifying options.'
)

parser.add_argument(
    'target',
    metavar='DOMAIN',
    type=str,
    help='Domain name or file with name list, one per line'
)

scan_choices = 'subdomains, crimeflare, mx'
parser.add_argument(
    '--scan',
    metavar='OPTION',
    nargs='*',
    choices=scan_choices.split(', '),
    default='subdomains crimeflare mx',
    help=scan_choices
)

parser.add_argument(
    '--sub',
    metavar='SUBDOMAIN',
    nargs='*',
    help='Scan specified subdomains'
)

args = parser.parse_args()
