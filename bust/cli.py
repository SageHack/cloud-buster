import argparse
from panels import PANELS

parser = argparse.ArgumentParser(
    description='Default behavior is scan everything.'
    + ' you can change that by specifying options.'
)

parser.add_argument(
    'target',
    metavar='DOMAIN_NAME',
    type=str
)

scan_choices = 'subdomains, panels, crimeflare'
parser.add_argument(
    '--scan',
    metavar='OPTION',
    nargs='*',
    choices=scan_choices.split(', '),
    default=scan_choices.split(', '),
    help=scan_choices
)

parser.add_argument(
    '--sub',
    metavar='SUBDOMAIN',
    nargs='*',
    help='Scan specified subdomains'
)


panel_list = [pan['name'] for pan in PANELS]
parser.add_argument(
    '--pan',
    metavar='PANEL',
    nargs='*',
    help=str(panel_list)
)

args = parser.parse_args()
