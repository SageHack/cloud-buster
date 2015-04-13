# cloudflare-resolver
A security tool that aim at doing the following
* Check if domains or ips are part of the CloudFlare network
* Scan domains for know vulnerabilities that allow to find ip
* Dictionary scan subdomains to find ips outside of CF network

# Tested OSes
* Debian
* Ubuntu

# How to use (debian/ubuntu)
* sudo apt-get install python3
* git clone https://github.com/SageHack/cloudflare-resolver.git
* cd cloud-buster
* python3 bust -h

# Installing DNS Python (debian/ubuntu)
* Visit http://www.dnspython.org
* Click Python 3.x Stable
* Download latest package
* Unzip/Untar
* Term in unziped directory
* sudo python3 setup.py install
