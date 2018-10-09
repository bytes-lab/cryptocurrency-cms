import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *

QBTAGGXref.objects.update(is_deleted=True)

for ii in MasterCoin.objects.filter(type_is_crypto=True, alias__isnull=True):
    for iii in QBTAGGQuote.objects.filter(is_deleted=False):
        if ii.id != iii.coin.id:
            source = ''
            if ii.cryptocompare > 0:
                source = 'cryptocompare'
            elif ii.coingecko > 0:
                source = 'coingecko'

            if source:
                defaults = {
                    'source': source,
                    'is_deleted': False
                }

                QBTAGGXref.objects.update_or_create(base_coin=ii, 
                                                    quote_coin=iii.coin, 
                                                    defaults=defaults)
