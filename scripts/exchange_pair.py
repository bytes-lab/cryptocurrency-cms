import json
import requests

import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *

def main():
    for exchange in Exchange.objects.filter(supported=True):
        all_pairs = {}
        for pair in ExchangePairXref.objects.filter(exchange=exchange.name):
            pair_ = '{}-{}'.format(pair.base_coin, pair.quote_coin)
            all_pairs[pair_] = pair.id

        try:
            pairs = requests.get(exchange.api_link).json()['data']
        except Exception as e:
            pairs = []

        for ii in pairs:
            pair_ = '{}-{}'.format(ii['baseCurrency'], ii['quoteCurrency'])
            if pair_ in all_pairs:
                all_pairs.pop(pair_)

            ExchangePairXref.objects.update_or_create(exchange=exchange.name, 
                                                      base_coin=ii['baseCurrency'], 
                                                      quote_coin=ii['quoteCurrency'])
        if all_pairs:
            ExchangePairXref.objects.filter(id__in=all_pairs.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
