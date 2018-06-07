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
        for pair in ExchangePairXref.objects.filter(exchange=exchange.name, is_deleted=False):
            pair_ = '{}-{}'.format(pair.base_coin, pair.quote_coin)
            all_pairs[pair_] = pair.id

        try:
            pairs = requests.get(exchange.api_link).json()['data'] or []
        except Exception as e:
            pairs = []

        for ii in pairs:
            pair_ = '{}-{}'.format(ii['baseCurrency'], ii['quoteCurrency'])
            if pair_ in all_pairs:
                all_pairs.pop(pair_)

            cc_support = CryptocomparePair.objects.filter(Q(exchange__iexact=exchange.cryptocompare) &
                                                         (Q(base_coin=ii['baseCurrency']) |
                                                          Q(quote_coin=ii['quoteCurrency']))).exists()
            cp_support = CoinapiPair.objects.filter(Q(exchange__iexact=exchange.coinapi) &
                                                     (Q(base_coin=ii['baseCurrency']) |
                                                      Q(quote_coin=ii['quoteCurrency']))).exists()

            ExchangePairXref.objects.update_or_create(exchange=exchange.name, 
                                                      base_coin=ii['baseCurrency'], 
                                                      quote_coin=ii['quoteCurrency'],
                                                      defaults={ 
                                                        'is_deleted': False,
                                                        'cryptocompare_availability': cc_support,
                                                        'coinapi_availability': cp_support 
                                                      })
        if all_pairs:
            ExchangePairXref.objects.filter(id__in=all_pairs.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()
