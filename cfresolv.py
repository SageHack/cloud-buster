from ipaddress import IPv4Network
from ipaddress import IPv6Network


class CF_Detect:

    IPV4_NETWORK = [
        IPv4Network(network)
        for network
        in open('ips-v4').read().splitlines()
    ]

    IPV6_NETWORK = [
        IPv6Network(network)
        for network
        in open('ips-v6').read().splitlines()
    ]

    def __init__(self):
        return None

    def in_range(self, ip):
        print(self.IPV4_NETWORK)
        print(self.IPV6_NETWORK)


cf = CF_Detect()
cf.in_range('127.0.0.1')
