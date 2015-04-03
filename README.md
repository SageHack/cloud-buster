# cloudflare-resolver
A CloudFlare resolver in Python that will someday support scanning via Tor (with Stem)

# Bla bla bla
This projet will use Python, Stem probably Flask (still unsure)
https://www.python.org/
https://stem.torproject.org/
http://flask.pocoo.org/

# CouldFlare documentation useful to the project
https://www.cloudflare.com/ips
https://www.cloudflare.com/ips-v4
https://www.cloudflare.com/ips-v6

# Ip Address module
https://docs.python.org/3/howto/ipaddress.html
https://docs.python.org/3/library/ipaddress.html#module-ipaddress

# Basic usage idea
cloudflare-resolver
  -d --domain # Specify main domain, can be anything that's a legal URL
  -t --tor # Proxy request trought tor
  -s --subdomains <file> # Check additionnal subdomains listed in a file
