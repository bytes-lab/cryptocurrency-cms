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

def get_coins():
    coins = {}
    for coin in MasterCoin.objects.all():
        coins[coin.symbol] = coin.id
    return coins

def add_coin(coin):
    send_email(coin, False, 'Cryptocompare')
    MasterCoin.objects.create(symbol=coin, is_trading=True, cryptocompare=1)
    return get_coins()
    
def main():
    url = 'https://min-api.cryptocompare.com/data/all/exchanges'
    info = requests.get(url).json()

    coins = get_coins()

    for key, val in info.items():
        defaults = {
            "cryptocompare": key
        }

        exchange, is_new = Exchange.objects.update_or_create(name=key.upper(), defaults=defaults)

        for base, quotes in val.items():
            for quote in quotes:
                if base not in coins:
                    coins = add_coin(base)
                if quote not in coins:
                    coins = add_coin(quote)

                pair, is_new = ExchangePair.objects.update_or_create(exchange=exchange, 
                                                                     base_coin_id=coins[base],
                                                                     quote_coin_id=coins[quote],
                                                                     defaults={
                                                                        "cryptocompare_availability": True
                                                                     })


if __name__ == "__main__":
    main()
