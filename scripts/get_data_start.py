import json
import time
import requests
import datetime

import os
from os import sys, path
import django
import urllib

base_url = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(base_url)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
from django.db import connection

def main():
    for ii in ExchangePair.objects.filter(data_start__isnull=True):
        ex = 'old_binance' if ii.exchange.name == 'BINANCE' else ii.exchange.name.lower()
        col = 'time' if ex in ['bittrex', 'kucoin'] else 'open_time'
        query = "SELECT {0} FROM {1}_rates WHERE base_currency_id = %s and quote_currency_id = %s order by {0} limit 1".format(col, ex)
        with connection.cursor() as cursor:
            cursor.execute(query, [ii.base_coin_id, ii.quote_coin_id])
            # to avoid post save
            data_start = cursor.fetchone()
            if data_start:
                ExchangePair.objects.filter(id=ii.id).update(data_start=data_start[0])

if __name__ == "__main__":
    main()
