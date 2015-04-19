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

# Exemples
* python3 bust mydomain.com
* python3 bust mydomain.com --scan crimeflare
* python3 bust mydomain.com --scan subdomains mx
* python3 bust mydomain.com --scan subdomains --sub www www2 ftp direct
* python3 bust mydomain.com --scan panels --pan cpanel cpanel:ssl whm
* python3 bust domainlist.txt
* python3 bust domainlist.txt (with any other options)

# Using domain lists
Use a text file with one domain per line, nothing else
