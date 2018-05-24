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
    url = 'https://min-api.cryptocompare.com/data/all/exchanges'
    info = requests.get(url).json()

    coins = [ii.symbol for ii in CryptocompareCoin.objects.all()]

    for key, val in info.items():
        defaults = {
            "cryptocompare": key
        }

        exchange, is_new = Exchange.objects.update_or_create(name=key.upper(), defaults=defaults)

        for base, quotes in val.items():
            if base not in coins:
                continue

            for quote in quotes:
                if quote not in coins:
                    continue

                pair, is_new = CryptocomparePair.objects.update_or_create(exchange=key.upper(),
                                                                          base_coin=base, 
                                                                          quote_coin=quote)


if __name__ == "__main__":
    main()
