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
from django.db.models import Q
from utils import send_email

def main():
    headers = { 'X-CoinAPI-Key': settings.COINAPI_KEY }
    url = 'https://rest.coinapi.io/v1/symbols'
    info = requests.get(url, headers=headers).json()

    coins = [ii.symbol for ii in CoinapiCoin.objects.all()]
    exchanges = [ii.coinapi for ii in Exchange.objects.all() if ii.coinapi]

    all_pairs = {}
    for pair in CoinapiPair.objects.all():
        pair_ = '{}-{}-{}'.format(pair.exchange, pair.base_coin, pair.quote_coin)
        all_pairs[pair_] = pair.id

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

        pair_ = '{}-{}-{}'.format(exchange, base, quote)
        if pair_ in all_pairs:
            all_pairs.pop(pair_)

        pair, is_new = CoinapiPair.objects.update_or_create(exchange=exchange, 
                                                            base_coin=base,
                                                            quote_coin=quote,
                                                            symbol_id=pair['symbol_id'],
                                                            market_type=pair['symbol_type'],
                                                            defaults={ 'is_deleted': False })
    if all_pairs:
        CoinapiPair.objects.filter(id__in=all_pairs.values()).update(is_deleted=True)

    # update cc, cp availability
    true_ids = []
    false_ids = []

    for ii in ExchangePair.objects.all():
        cp_support = CoinapiPair.objects.filter(Q(exchange__iexact=ii.exchange.coinapi) &
                                                 (Q(base_coin=ii.base_coin.original_symbol) |
                                                  Q(quote_coin=ii.quote_coin.original_symbol))).exists()

        if cp_support:
            true_ids.append(ii.id)
        else:
            false_ids.append(ii.id)

    ExchangePair.objects.filter(id__in=true_ids).update(coinapi_availability=True)
    ExchangePair.objects.filter(id__in=false_ids).update(coinapi_availability=False)

if __name__ == "__main__":
    main()
