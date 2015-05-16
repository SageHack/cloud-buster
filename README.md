# cloudflare-resolver
A security tool that aim at doing the following
* Check if domains or ips are part of the CloudFlare network
* Scan domains for know vulnerabilities that allow to find ip
* Dictionary scan subdomains to find ips outside of CF network

# Examples
* python3 lists/update.py
* python3 bust mydomain.com
* python3 bust mydomain.com --scan crimeflare
* python3 bust mydomain.com --scan subdomains mx
* python3 bust mydomain.com --scan subdomains --sub www www2 ftp direct
* python3 bust mydomain.com --dept normal
* python3 bust domainlist.txt (with any other options)
* python3 bust mydomain.com --dept full

# Using domain lists
Use a text file with one domain per line, nothing else

# Updating lists
CrimeFlare DB is updated every two weeks, the GitHub repo might not be up to date with the latest list. You should use the update tool to get the latests lists.

# Tested OSes
* Debian
* Ubuntu
* Arch
* Void
* Parabola

# How to use (Ubuntu)
* sudo apt-get install python3 python3-pip
* pip3 install dnspython3
* git clone https://github.com/SageHack/cloudflare-resolver.git
* cd cloud-buster
* python3 bust -h

# How to use (Debian)
* su root
* apt-get remove python3
* apt-get autoremove
* apt-get update
* apt-get install libssl-dev openssl
* cd /opt
* wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
* tar xzf Python-3.4.3.tgz
* cd Python-3.4.3
* ./configure
* make
* sudo make install
* rm *.tgz
* rm -fr Python-3.4.3/
* ln -s /usr/local/bin/python3 /usr/bin/python3
* pip3 install dnspython3
* # Open new terminal window
* git clone https://github.com/SageHack/cloudflare-resolver.git
* cd cloud-buster
* python3 bust -h

# How to use (Void)
* xbps-install python3 python-pip
* pip install dnspython3
* git clone https://github.com/SageHack/cloudflare-resolver.git
* cd cloud-buster
* python3 bust -h

# How to use (Arch and Parabola)
* pacman -Sy python python-pip
