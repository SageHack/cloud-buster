import urllib.request
import zipfile
import os
import sys
import time

class Updater:
    def run():
        if Updater.uptodate():
            return

        downloads = [
            ['https://www.cloudflare.com/ips-v4', 'lists/cloudflare_ipv4'],
            ['https://www.cloudflare.com/ips-v6', 'lists/cloudflare_ipv6'],
        ]

        for d in downloads:
            Updater.download(d[0], d[1])

        Updater.last_updated(Updater.today())
        print('')


    def uptodate():
        last_updated = open('lists/last_updated', 'r').read()
        if last_updated == Updater.today():
            return True
        return False

    def last_updated(date):
        file = open('lists/last_updated', 'w')
        file.write(date)
        file.close

    def today():
        return time.strftime("%Y-%m-%d")

    def download(url, file):
        print('[download] %s' % url)
        try:
            urllib.request.urlretrieve(url, file)
        except (OSError, HTTPError, http.client.BadStatusLine):
            pass
