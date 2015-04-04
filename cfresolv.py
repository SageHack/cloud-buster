from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network


class CF_Detect:

    IPV4_NETWORKS = [
        IPv4Network(network)
        for network
        in open('ips-v4').read().splitlines()
    ]

    IPV6_NETWORKS = [
        IPv6Network(network)
        for network
        in open('ips-v6').read().splitlines()
    ]

    def in_range(self, ip):
        address = self.instantiate_address(ip)
        if not address:
            return False

        if address.version == 4:
            networks = self.IPV4_NETWORKS
        else:
            networks = self.IPV6_NETWORKS

        return self.in_network(address, networks)

    def in_network(self, host, networks):
        for network in networks:
            if host in network:
                return True

        return False

    def instantiate_address(self, ip):
        try:
            return IPv4Address(ip)
        except:
            try:
                return IPv6Address(ip)
            except:
                return None


cf = CF_Detect()
print(cf.in_range('adfasdf'))
print(cf.in_range(''))
print(cf.in_range('172.71.255.250'))
print(cf.in_range('250.71.255.250'))
print(cf.in_range('2400:cb00::5e:b4da'))
print(cf.in_range('9400:cb00::5e:b4da'))
