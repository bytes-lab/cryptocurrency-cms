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
from django.conf import settings

def get_coins():
    coins = {}
    for coin in MasterCoin.objects.all():
        coins[coin.symbol] = coin.id
    return coins

def add_coin(coin):
    MasterCoin.objects.create(symbol=coin, is_trading=True, cryptocompare=1)
    return get_coins()

def get_exchanges():
    exchanges = {}
    for exchange in Exchnage.objects.all():
        exchanges[exchange.name] = exchange.id
    return exchanges

def add_exchnage(exchange):
    Exchnage.objects.create(name=exchange, coinapi=exchange)
    return get_exchanges()

def main():
    headers = { 'X-CoinAPI-Key': settings.COINAPI_KEY }
    url = 'https://rest.coinapi.io/v1/symbols'
    info = requests.get(url, headers=headers).json()

    coins = get_coins()
    exchanges = get_exchanges()

    for pair in info:
        base = pair['asset_id_base']
        quote = pair['asset_id_quote']
        exchange = pair['exchange_id']

        if exchange not in exchanges:
            exchanges = add_exchnage(exchange)
        if base not in coins:
            coins = add_coin(base)
        if quote not in coins:
            coins = add_coin(quote)

        defaults = {
            "coinapi_availability": True
            "website_url": pair.get('website'),
            "data_start": parse_date(pair.get('data_start')),
            "data_end": parse_date(pair.get('data_end'))
        }

        pair, is_new = ExchangePair.objects.update_or_create(exchange_id=exchanges[exchange], 
                                                             base_coin_id=coins[base],
                                                             quote_coin_id=coins[quote],
                                                             defaults=defaults)

def parse_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d') if str_date else None

def parse_datetime(str_datetime):
    if str_datetime:
        return datetime.datetime.strptime(str_datetime.split(".")[0], '%Y-%m-%dT%H:%M:%S')

if __name__ == "__main__":
    main()
