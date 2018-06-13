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
    all_coins = {}
    for coin in CoingeckoCoin.objects.filter(is_deleted=False):
        all_coins[coin.uid] = coin.id

    page = 1
    while True:
        url = 'https://api.coingecko.com/api/v3/coins/?per_page=250&page={}'.format(page)
        info = requests.get(url).json()
        if not info:
            break

        page = page + 1
        for coin in info:
            if coin['id'] in all_coins:
                all_coins.pop(coin['id'])

            defaults = {
                "name": coin.get('name'),
                "symbol": coin.get('symbol'),
                "is_deleted": False
            }

            coin, is_new = CoingeckoCoin.objects.update_or_create(uid=coin['id'], defaults=defaults)
            # if is_new:
            #     send_email(coin['asset_id'], True, 'Coinapi')

    if all_coins:
        CoingeckoCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
