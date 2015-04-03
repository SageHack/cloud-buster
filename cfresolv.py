from ipaddress import IPv4Network
from ipaddress import IPv6Network


class CF_Detect:

    # Source : https://www.cloudflare.com/ips-v4
    CLOUDFLARE_IPV4 = (
        IPv4Network('199.27.128.0/21'),
        IPv4Network('173.245.48.0/20'),
        IPv4Network('103.21.244.0/22'),
        IPv4Network('103.22.200.0/22'),
        IPv4Network('103.31.4.0/22'),
        IPv4Network('141.101.64.0/18'),
        IPv4Network('108.162.192.0/18'),
        IPv4Network('190.93.240.0/20'),
        IPv4Network('188.114.96.0/20'),
        IPv4Network('197.234.240.0/22'),
        IPv4Network('198.41.128.0/17'),
        IPv4Network('162.158.0.0/15'),
        IPv4Network('104.16.0.0/12'),
        IPv4Network('172.64.0.0/13'),
    )

    # Source : https://www.cloudflare.com/ips-v6
    CLOUDFLARE_IPV6 = (
        IPv6Network('2400:cb00::/32'),
        IPv6Network('2606:4700::/32'),
        IPv6Network('2803:f800::/32'),
        IPv6Network('2405:b500::/32'),
        IPv6Network('2405:8100::/32'),
    )

    def in_range(self, ip):
        print(self.CLOUDFLARE_IPV4)
        print(self.CLOUDFLARE_IPV6)


cf = CF_Detect()
cf.in_range('127.0.0.1')
