import json
import time
import requests
import hmac
import hashlib
import datetime

import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
from django.db.models import Q
from django.conf import settings
from utils import send_email

def main():
    BASE_URL = 'https://api.coinigy.com'
    ENDPOINT = '/api/v2/private/markets'
    X_API_KEY = '271bf6888ab443579a5a86a6855ea215'
    SECRET = '113cee19526745d5bb7eaf831e678919'
    METHOD = 'GET'
    UNIXTIME = time.time()
    PARAMS = {}  # = {'StartDate':'2018-07-30T00:00:00.000Z','EndDate':'2018-07-30T23:59:59.000Z'}
    BODY = ''

    X_API_TIMESTAMP = str(int(UNIXTIME))
    msg = X_API_KEY + X_API_TIMESTAMP + METHOD + ENDPOINT + BODY
    signature_bytes = hmac.new(SECRET.encode("ascii"), msg.encode("ascii"), digestmod=hashlib.sha256).digest()
    signature_hex = map("{:02X}".format, bytearray(signature_bytes))
    # python3 way
    # signature_hex = map("{:02X}".format, signature_bytes)
    X_API_SIGN = ''.join(signature_hex)

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-API-SIGN': X_API_SIGN,
               'X-API-TIMESTAMP': X_API_TIMESTAMP, 'X-API-KEY': X_API_KEY}
    r = requests.get(BASE_URL + ENDPOINT, headers=headers, params=PARAMS, data=BODY)
    if r.status_code == 200:
        content = json.loads(r.content)
        if content['success']:
            info = content['result']
            coins = [ii.symbol for ii in CoinigyCoin.objects.all()]
            exchanges = [ii.name for ii in Exchange.objects.all()]
            all_pairs = {}
            for pair in CoinigyPair.objects.all():
                pair_ = '{}-{}-{}'.format(pair.exchange, pair.base_coin, pair.quote_coin)
                all_pairs[pair_] = pair.id

            for pair in info:
                base = pair['baseCurrCode']
                quote = pair['quoteCurrCode']
                exchange = pair['exchCode']
                # print(pair)
                if exchange not in exchanges:
                    continue
                if base not in coins:
                    continue
                if quote not in coins:
                    continue

                pair_ = '{}-{}-{}'.format(exchange, base, quote)
                print(pair_)
                if pair_ in all_pairs:
                    all_pairs.pop(pair_)

                pair, is_new = CoinigyPair.objects.update_or_create(exchange=exchange,
                                                                    base_coin=base,
                                                                    quote_coin=quote,
                                                                    defaults={'is_deleted': False})
            if all_pairs:
                CoinigyPair.objects.filter(id__in=all_pairs.values()).update(is_deleted=True)

            # update cc, cp availability
            true_ids = []
            false_ids = []

            for ii in ExchangePair.objects.all():
                cp_support = CoinigyPair.objects.filter(Q(exchange__iexact=ii.exchange.name) &
                                                        (Q(base_coin=ii.base_coin.original_symbol) |
                                                         Q(quote_coin=ii.quote_coin.original_symbol))).exists()

                if cp_support:
                    true_ids.append(ii.id)
                else:
                    false_ids.append(ii.id)

            ExchangePair.objects.filter(id__in=true_ids).update(coinigy_availability=True)
            ExchangePair.objects.filter(id__in=false_ids).update(coinigy_availability=False)


if __name__ == "__main__":
    main()
