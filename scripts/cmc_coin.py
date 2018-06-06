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
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
    info = requests.get(url).json()

    all_coins = {}
    for coin in CoinmarketcapCoin.objects.filter(is_deleted=False):
        all_coins[coin.token] = coin.id

    for coin in info:
        if coin['id'] in all_coins:
            all_coins.pop(coin['id'])

        defaults = {
            "symbol": coin['symbol'],
            "is_deleted": False
        }

        coin, is_new = CoinmarketcapCoin.objects.update_or_create(token=coin['id'], defaults=defaults)
        # if is_new:
        #     send_email(coin['symbol'], True, 'Coinmarketcap')

    if all_coins:
        CoinmarketcapCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
