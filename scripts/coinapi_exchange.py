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

def main():
    headers = { 'X-CoinAPI-Key': settings.COINAPI_KEY }
    url = 'https://rest.coinapi.io/v1/exchanges'
    info = requests.get(url, headers=headers).json()

    for exchange in info:
        defaults = {
            "website_url": exchange.get('website'),
            "company": exchange.get('name'),
            "data_start": parse_date(exchange.get('data_start')),
            "data_end": parse_date(exchange.get('data_start')),
            "data_quote_start": parse_datetime(exchange.get('data_quote_start')),
            "data_quote_end": parse_datetime(exchange.get('data_quote_end')),
            "data_orderbook_start": parse_datetime(exchange.get('data_orderbook_start')),
            "data_orderbook_end": parse_datetime(exchange.get('data_orderbook_end')),
            "data_trade_start": parse_datetime(exchange.get('data_trade_start')),
            "data_trade_end": parse_datetime(exchange.get('data_trade_end')),
            "data_trade_count": exchange.get('data_trade_count') or None,
            "data_symbols_count": exchange.get('data_symbols_count') or None,
            "coinapi": 1
        }
        exchange, is_new = CoinapiExchange.objects.update_or_create(name=exchange['exchange_id'], defaults=defaults)

def parse_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d') if str_date else None

def parse_datetime(str_datetime):
    if str_datetime:
        return datetime.datetime.strptime(str_datetime.split(".")[0], '%Y-%m-%dT%H:%M:%S')

if __name__ == "__main__":
    main()
