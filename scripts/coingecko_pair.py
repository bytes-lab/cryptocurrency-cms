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
    url = 'https://api.coingecko.com/api/v3/exchanges'
    exchanges = [ii.coingecko for ii in Exchange.objects.all() if ii.coingecko and ii.name]
    print(len(exchanges))
    # for exchange in exchanges:




if __name__ == "__main__":
    main()
