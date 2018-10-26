import json
import requests
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
    BASE_URL = 'https://api.coinigy.com'
    ENDPOINT = '/api/v2/public/chains'
    PARAMS = {}  # = {'StartDate':'2018-07-30T00:00:00.000Z','EndDate':'2018-07-30T23:59:59.000Z'}
    BODY = {}
    headers = {}
    r = requests.get(BASE_URL + ENDPOINT, headers=headers, params=PARAMS, data=BODY)
    if r.status_code == 200:
        content = json.loads(r.content)
        if content['success']:
            info = content['result']
            all_coins = {}
            for coin in CoinigyCoin.objects.filter(is_deleted=False):
                all_coins[coin.symbol] = coin.id

            for coin in info:
                if coin['currCode'] in all_coins:
                    all_coins.pop(coin['currCode'])

                defaults = {
                    "name": coin.get('currName'),
                    "is_deleted": False
                }

                coin, is_new = CoinigyCoin.objects.update_or_create(symbol=coin['currCode'], defaults=defaults)
                # if is_new:
                #     send_email(coin['asset_id'], True, 'Coinapi')

            if all_coins:
                CoinigyCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)

if __name__ == "__main__":
    main()
