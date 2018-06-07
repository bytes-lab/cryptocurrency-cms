import json
import time
import requests
import datetime

import os
from os import sys, path
import django
import urllib

base_url = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(base_url)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
from utils import send_email

sizes = [16, 32, 48, 64, 128]

def main():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    coins = requests.get(url).json().get('Data', {})
    headers = { 'cookie': '__cfduid=d4f723e7ca0160143b1c13ac7bf1819741528343396; _tuts_session=d04a378a2fdc02aa0b2fdf22d285452a; _ga=GA1.2.2058121609.1528343396; _gid=GA1.2.541871630.1528343396; __gads=ID=e0ebfc441b1d895d:T=1528343400:S=ALNI_MZpYcNa89niIKwttMQ54vlOpzhdyQ' }

    for key, val in coins.items():
        url = val.get('ImageUrl')
        if not url:
            continue
        url_ = "https://www.cryptocompare.com" + url

        coin = CryptocompareCoin.objects.filter(symbol=val.get('Symbol')).first()
        if not coin:
            continue
        coin = MasterCoin.objects.filter(cryptocompare=coin.id).first()
        if not coin:
            continue

        for size in sizes:
            url = url_ + '?width={}'.format(size)
            file_name = coin.symbol.replace('*', 'star')
            file_path = base_url + '/static/icons/{}-{}.png'.format(file_name, size)
            print url, file_path
            info = requests.get(url, headers=headers)
            with open(file_path, "wb") as file:
                file.write(info.content)


if __name__ == "__main__":
    main()
