# Cloudflare Resolver

A comprehensive pentest tool that checks Cloudflare enabled sites for origin IP leaks.

It's filled with awesome features!

* scan a wide array of miss-configuration and vulnerabilities
* detail origin IP and related services IPs
* smart(ish) engine that can certify matches
* multiple command line arguments to customize and fine tune
* scan any number of targets
* still maintained and improved

![Screenshot](/screenshot.png?raw=true "Usage example")

## Requirements
 * [Python 3.5](https://www.python.org/downloads/release/python-350/)
 * [dnspython3 1.14.0](http://www.dnspython.org/kits3/1.14.0/)
 * libssl
 * openssl

## Usage

### Basic use cases
* Run the fast/simple scan
* `python3 bust mydomain.com`
* Run the slow/comprehensive scan
* `python3 bust mydomain.com --scan mx crimeflare dnsdumpster subdomain --dept normal`
* Scan multiple domains
* `python3 bust domainlist.txt` (with any options)

### Complex use cases
* Use a single scan technique
* `python3 bust mydomain.com --scan crimeflare`
* Chose your own mix of scan techniques
* `python3 bust mydomain.com --scan subdomain mx`
* Scan specific subdomains
* `python3 bust mydomain.com --scan subdomain --sub www www2 ftp direct`
* Scan the 20,000 most popular subdomains on the net
* `python3 bust mydomain.com --dept full`

### Using domain lists
Use a text file with one domain per line, nothing else

### Updating lists
CrimeFlare DB is updated every two weeks, the GitHub repo might not be up to date with the latest list. You should use the update tool to get the latest lists.

### Tor

Since Cloudflare is very good at blocking Tor with CAPTCHAs, using this tool over Tor is pretty much useless.

## Installation

### Ubuntu
```
sudo apt-get install python3 python3-pip
pip3 install dnspython3 bs4
git clone https://github.com/SageHack/cloud-buster.git
cd cloud-buster
python3 bust -h
```

### Debian 9
```
su
apt install python3-pip
pip3 install dnspython3 bs4
git clone https://github.com/SageHack/cloud-buster.git
cd cloud-buster
python3 bust -h
```

### Debian 8
```
su root
apt-get remove python3
apt-get autoremove
apt-get update
apt-get install libssl-dev openssl
cd /opt
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar xzf Python-3.4.3.tgz
cd Python-3.4.3
./configure
make
sudo make install
rm *.tgz
rm -fr Python-3.4.3/
ln -s /usr/local/bin/python3 /usr/bin/python3
pip3 install dnspython3 bs4
# Open new terminal window
git clone https://github.com/SageHack/cloud-buster.git
cd cloud-buster
python3 bust -h
```

### Void
```
xbps-install python3 python-pip
pip install dnspython3 bs3
git clone https://github.com/SageHack/cloud-buster.git
cd cloud-buster
python3 bust -h
```

### Arch and Parabola
```
pacman -Sy python python-pip
pip install dnspython3 bs3
git clone https://github.com/SageHack/cloud-buster.git
cd cloud-buster
python3 bust -h
```

## Contributing

The current tested version is Python 3.5.3.
Please use this version to submit pull requests.

Otherwise, all other requirements are listed above.
