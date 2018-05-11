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
            "coinapi": exchange['exchange_id'],
            "website_url": exchange.get('website')
        }
        exchange, is_new = Exchange.objects.update_or_create(name=exchange['exchange_id'], defaults=defaults)

def parse_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d') if str_date else None

def parse_datetime(str_datetime):
    if str_datetime:
        return datetime.datetime.strptime(str_datetime.split(".")[0], '%Y-%m-%dT%H:%M:%S')

if __name__ == "__main__":
    main()
