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

def main():
    url = 'https://min-api.cryptocompare.com/data/all/exchanges'
    info = requests.get(url).json()

    coins = {}
    for coin in MasterCoin.objects.all():
        coins[coin.symbol] = coin.id

    for key, val in info.items():
        defaults = {
            "cryptocompare": 1
        }

        exchange, is_new = CryptocompareExchange.objects.update_or_create(name=key.upper(), defaults=defaults)

        for base, quotes in val.items():
            base = 'USDT' if base == 'USD' else base

            for quote in quotes:
                quote = 'USDT' if quote == 'USD' else quote
                if quote in coins and base in coins:
                    pair, is_new = ExchangePair.objects.update_or_create(exchange=exchange, 
                                                                         base_coin_id=coins[base],
                                                                         quote_coin_id=coins[quote],
                                                                         defaults={
                                                                            "cryptocompare_availability": True
                                                                         })
                else:
                    print base if quote in coins else quote, '##########'


if __name__ == "__main__":
    main()
