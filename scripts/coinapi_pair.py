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
    url = 'https://rest.coinapi.io/v1/symbols'
    info = requests.get(url, headers=headers).json()

    coins = [ii.symbol for ii in CoinapiCoin.objects.all()]
    exchanges = [ii.coinapi for ii in Exchange.objects.all() if ii.coinapi]

    for pair in info:
        base = pair['asset_id_base']
        quote = pair['asset_id_quote']
        exchange = pair['exchange_id']

        if exchange not in exchanges:
            continue
        if base not in coins:
            continue
        if quote not in coins:
            continue

        pair, is_new = CoinapiPair.objects.update_or_create(exchange=exchange, 
                                                            base_coin=base,
                                                            quote_coin=quote,
                                                            symbol_id=pair['symbol_id'],
                                                            market_type=pair['symbol_type'])

if __name__ == "__main__":
    main()
