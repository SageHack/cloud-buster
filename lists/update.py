import urllib.request
import zipfile
import os
import sys

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
    if readsofar >= totalsize:  # near the end
        sys.stderr.write("\n")

print('Downloading Cloudflare IPV4 ip list')
urllib.request.urlretrieve('https://www.cloudflare.com/ips-v4', 'ips-v4')

print('Downloading Cloudflare IPV6 ip lists')
urllib.request.urlretrieve('https://www.cloudflare.com/ips-v6', 'ips-v6')

print('Downloading latest subdomain list from GitHub repo')
urllib.request.urlretrieve(
    'https://raw.githubusercontent.com/SageHack/cloud-buster/master/lists/subdomains',
    'subdomains'
)

print('Downloading latest CrimeFlare DB, this might take one or two minutes')
urllib.request.urlretrieve(
    'http://www.crimeflare.com/domains/ipout.zip',
    'ipout.zip',
    reporthook
)
with zipfile.ZipFile('ipout.zip', 'w') as myzip:
    myzip.write('ipout')
os.remove('ipout.zip')

print('Everything up to date!')
