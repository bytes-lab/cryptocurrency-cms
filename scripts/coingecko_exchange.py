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
    api = 'https://api.coingecko.com/api/v3/exchanges'
    r = requests.get(api)
    if r.status_code == 200:
        content = json.loads(r.content)
        for exchange in content:
            obj = Exchange.objects.filter(
                Q(name=exchange['name'].upper()) | Q(name=exchange['id'].upper())).first()
            if not obj:
                Exchange.objects.create(name=exchange['name'].upper())
            else:
                Exchange.objects.filter(id=obj.id).update(coingecko=exchange['id'])
            # consider more about possible minor differences over same exchanges

if __name__ == "__main__":
    main()
