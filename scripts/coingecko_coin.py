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
from utils import send_email

def main():
    headers = { 'X-CoinAPI-Key': settings.COINAPI_KEY }
    url = 'https://rest.coinapi.io/v1/assets'
    info = requests.get(url, headers=headers).json()

    all_coins = {}
    for coin in CoinapiCoin.objects.filter(is_deleted=False):
        all_coins[coin.symbol] = coin.id

    for coin in info:
        if coin['asset_id'] in all_coins:
            all_coins.pop(coin['asset_id'])

        defaults = {
            "name": coin.get('name'),
            "is_deleted": False
        }

        coin, is_new = CoinapiCoin.objects.update_or_create(symbol=coin['asset_id'], defaults=defaults)
        # if is_new:
        #     send_email(coin['asset_id'], True, 'Coinapi')

    if all_coins:
        CoinapiCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
