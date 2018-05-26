import json
import time
import requests
import datetime

import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
from utils import send_email

def main():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    coins = requests.get(url).json().get('Data', {})

    for key, val in coins.items():
        defaults = {
            'name': val.get('Name'),
            'fullname': val.get('FullName')
        }

        coin, is_new = CryptocompareCoin.objects.update_or_create(symbol=val.get('Symbol'), defaults=defaults)
        if is_new:
            send_email(val.get('Symbol'), True, 'Cryptocompare')


if __name__ == "__main__":
    main()
