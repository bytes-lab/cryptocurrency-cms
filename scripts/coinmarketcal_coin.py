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

CLIENT_ID = '917_4rbbdcjtwuqsskoo8goow88088wkg0w0cscgs08s488w84s40w'
CLIENT_SECRET = '4vd1mse6sg00wg484scskssskswk0s800ksw0so804k4o8gss0'

def main():
    url = 'https://api.coinmarketcal.com/oauth/v2/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(CLIENT_ID, CLIENT_SECRET)
    access_token = requests.get(url).json()['access_token']

    all_coins = {}
    for coin in CoinmarketcalCoin.objects.filter(is_deleted=False):
        all_coins[coin.uid] = coin.id

    url = 'https://api.coinmarketcal.com/v1/coins?access_token={}'.format(access_token)
    info = requests.get(url).json()

    for coin in info:
        if coin['id'] in all_coins:
            all_coins.pop(coin['id'])

        defaults = {
            "name": coin.get('name'),
            "symbol": coin.get('symbol').upper(),
            "is_deleted": False
        }

        coin, is_new = CoinmarketcalCoin.objects.update_or_create(uid=coin['id'], defaults=defaults)
        # if is_new:
        #     send_email(coin['asset_id'], True, 'Coingecko')

    if all_coins:
        CoinmarketcalCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
