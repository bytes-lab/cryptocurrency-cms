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
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
    info = requests.get(url).json()

    for coin in info:
        defaults = {
            "coinmarketcap": coin['rank'],
            "is_master": True
        }

        coin, is_new = MasterCoin.objects.update_or_create(symbol=coin['symbol'], defaults=defaults)
        if is_new:
            send_email(coin['symbol'])

if __name__ == "__main__":
    main()
