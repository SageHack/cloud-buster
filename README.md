# cloudflare-resolver
A security tool that aim at doing the following
* Check if domains or ips are part of the CloudFlare network
* Scan domains for know vulnerabilities that allow to find ip
* Dictionary scan subdomains to find ips outside of CF network

# How to use (Linux)
* sudo apt-get install python3
* git clone https://github.com/SageHack/cloudflare-resolver.git
* cd cloud-buster
* python3 bust -h

# How to use (Windows)
* install python3.4
* git clone https://github.com/SageHack/cloudflare-resolver.git
* cd cloud-buster
* python3 bust -h

# Installing DNS Python
* Visit http://www.dnspython.org
* Click Python 3.x Stable
* Download dnspython3-x.xx.x.zip
* Unzip
* In terminal, browse to the unziped directory
* Windows: python3 setup.py install (as admin)
* Unix : sudo python3 setup.py install
