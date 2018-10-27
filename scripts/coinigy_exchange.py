import json
import requests

import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
from django.db.models import Q
from django.conf import settings

def main():
    BASE_URL = 'https://api.coinigy.com'
    ENDPOINT = '/api/v2/public/exchanges'
    PARAMS = {}  # = {'StartDate':'2018-07-30T00:00:00.000Z','EndDate':'2018-07-30T23:59:59.000Z'}
    BODY = {}
    headers = {}
    r = requests.get(BASE_URL + ENDPOINT, headers=headers, params=PARAMS, data=BODY)
    if r.status_code == 200:
        content = json.loads(r.content)
        if content['success']:
            info = content['result']
            for exchange in info:
                defaults = {
                    "coinigy": exchange['exchCode'],
                    # "website_url": exchange.get('exchUrl')
                }
                exchange, is_new = Exchange.objects.filter(Q(name=exchange['exchCode']) | Q(name=exchange['exchName'])).update_or_create(defaults=defaults)
                # consider more about possible minor differences over same exchanges

if __name__ == "__main__":
    main()
