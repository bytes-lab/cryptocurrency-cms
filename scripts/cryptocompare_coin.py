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

def main():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    coins = requests.get(url).json().get('Data', {})

    for key, val in coins.items():
        url_ = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={}'.format(val['Id'])
        info = requests.get(url_).json()['Data']['General']

        image_url = "https://www.cryptocompare.com"+val['ImageUrl'] if val.get('ImageUrl') else None
        launch_date = datetime.datetime.strptime(info['StartDate'], '%d/%m/%Y') if info.get('StartDate') and info.get('StartDate') != '01/01/0001' else None

        defaults = {
            'website_url': info.get('WebsiteUrl'),
            'image_url': image_url,
            'is_trading': val.get('IsTrading'),
            'sort_order': val.get('SortOrder') or -1,
            'cryptocompare': val['Id'],            
            'launch_date': launch_date,
            'algorithm': info.get('Algorithm'),
            'twitter_handle': info.get('Twitter'),
            'block_time': info.get('BlockTime') or -1,
            'proof_type': info.get('ProofType'),
            'block_reward': info.get('BlockReward')
        }

        MasterCoin.objects.update_or_create(symbol=val.get('Symbol'), defaults=defaults)


if __name__ == "__main__":
    main()
