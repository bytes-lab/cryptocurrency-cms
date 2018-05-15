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
    url = 'https://rest.coinapi.io/v1/assets'
    info = requests.get(url, headers=headers).json()

    for coin in info:
        defaults = {
            "coinapi": 1,
            "type_is_crypto": coin.get('type_is_crypto'),
            "is_master": True
        }

        coin, is_new = MasterCoin.objects.update_or_create(symbol=coin['asset_id'], defaults=defaults)


if __name__ == "__main__":
    main()
