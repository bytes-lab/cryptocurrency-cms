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

    all_coins = {}
    for coin in CryptocompareCoin.objects.filter(is_deleted=False):
        all_coins[coin.symbol] = coin.id

    for key, val in coins.items():
        if val.get('Symbol') in all_coins:
            all_coins.pop(val.get('Symbol'))

        defaults = {
            'name': val.get('Name'),
            'coinname': val.get('CoinName'),
            'fullname': val.get('FullName'),
            "is_deleted": False
        }

        coin, is_new = CryptocompareCoin.objects.update_or_create(symbol=val.get('Symbol'), defaults=defaults)
        # if is_new:
        #     send_email(val.get('Symbol'), True, 'Cryptocompare')
    if all_coins:
        CryptocompareCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
