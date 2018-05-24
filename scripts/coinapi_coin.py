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

    for coin in info:
        defaults = {
            "name": coin.get('name'),
        }

        coin, is_new = CoinapiCoin.objects.update_or_create(symbol=coin['asset_id'], defaults=defaults)
        if is_new:
            send_email(coin['asset_id'], True, 'Coinapi')


if __name__ == "__main__":
    main()
