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

from django.db.models import Q
from general.models import *
from utils import send_email

def main():
    url = 'https://min-api.cryptocompare.com/data/all/exchanges'
    info = requests.get(url).json()

    coins = [ii.symbol for ii in CryptocompareCoin.objects.all()]

    all_pairs = {}
    for pair in CryptocomparePair.objects.all():
        pair_ = '{}-{}-{}'.format(pair.exchange, pair.base_coin, pair.quote_coin)
        all_pairs[pair_] = pair.id

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

                pair_ = '{}-{}-{}'.format(key.upper(), base, quote)
                if pair_ in all_pairs:
                    all_pairs.pop(pair_)

                pair, is_new = CryptocomparePair.objects.update_or_create(exchange=key.upper(),
                                                                          base_coin=base, 
                                                                          quote_coin=quote,
                                                                          defaults={ 'is_deleted': False })
    if all_pairs:
        CryptocomparePair.objects.filter(id__in=all_pairs.values()).update(is_deleted=True)

    # update cc, cp availability
    true_ids = []
    false_ids = []

    for ii in ExchangePair.objects.all():
        cc_support = CryptocomparePair.objects.filter(Q(exchange__iexact=ii.exchange.cryptocompare) &
                                                 (Q(base_coin=ii.base_coin.original_symbol) |
                                                  Q(quote_coin=ii.quote_coin.original_symbol))).exists()
        if cc_support:
            true_ids.append(ii.id)
        else:
            false_ids.append(ii.id)

    ExchangePair.objects.filter(id__in=true_ids).update(cryptocompare_availability=True)
    ExchangePair.objects.filter(id__in=false_ids).update(cryptocompare_availability=False)


if __name__ == "__main__":
    main()
