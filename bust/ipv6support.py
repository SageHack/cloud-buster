from ipaddress import ip_address
from urllib.parse import urlparse, urljoin

"""
In an URL, IPv6 addresses must be surrounded by
square brackets due to ':' usage.
"""


class IPv6Support:
    def fix(ip):
        try:
            address = ip_address(ip)
        except ValueError:
            return ip

        if address.version == 6:
            return '['+ip+']'
        else:
            return ip
