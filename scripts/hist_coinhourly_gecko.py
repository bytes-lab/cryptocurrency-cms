import json
import time
import requests
from datetime import timedelta, date

import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
import pdb

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_start_date(coin, start_date_, end_date):
    result = CoinHourlyInfo.objects.filter(coin=coin, date_of_entry__gt=start_date_, date_of_entry__lt=end_date).order_by('date_of_entry').first()
    return result.date_of_entry.date() if result else start_date_

def main():
    start_date_ = date(2016, 1, 1)
    end_date = date(2018, 6, 15)
    for coin in MasterCoin.objects.all():
        hour_info = {}
        if coin.coingecko:
            start_date = get_start_date(coin, start_date_, end_date)
            for single_date in daterange(start_date, end_date):
                cg_coin = CoingeckoCoin.objects.get(id=coin.coingecko)
                url_ = 'https://api.coingecko.com/api/v3/coins/{}/history?date={}&localization=false'.format(cg_coin.uid, single_date.strftime("%d-%m-%Y"))
                info = requests.get(url_).json()
                print (url_, '-----------------------')
                # pdb.set_trace()
                if not info.get('community_data'):
                    continue
                print (coin.id, coin.symbol, single_date, '$$$$$$$$$$$$$$$$$$$$$')
                hour_info['facebook_likes'] = info.get('community_data')['facebook_likes']
                hour_info['twitter_followers'] = info.get('community_data')['twitter_followers']
                hour_info['reddit_subscribers'] = info.get('community_data')['reddit_subscribers']
                hour_info['reddit_average_posts_48h'] = info.get('community_data')['reddit_average_posts_48h']
                hour_info['reddit_average_comments_48h'] = info.get('community_data')['reddit_average_comments_48h']
                hour_info['reddit_accounts_active_48h'] = info.get('community_data')['reddit_accounts_active_48h']

                hour_info['repo_forks'] = info.get('developer_data')['forks']
                hour_info['repo_stars'] = info.get('developer_data')['stars']
                hour_info['repo_subscribers'] = info.get('developer_data')['subscribers']
                hour_info['repo_total_issues'] = info.get('developer_data')['total_issues']
                hour_info['repo_closed_issues'] = info.get('developer_data')['closed_issues']
                hour_info['repo_pull_requests_merged'] = info.get('developer_data')['pull_requests_merged']
                hour_info['repo_pull_request_contributors'] = info.get('developer_data')['pull_request_contributors']
                hour_info['repo_commit_count_4_weeks'] = info.get('developer_data')['commit_count_4_weeks']
                hour_info['alexa_rank'] = info.get('public_interest_stats')['alexa_rank']
                hour_info['bing_matches'] = info.get('public_interest_stats')['bing_matches']
                hour_info['date_of_entry'] = single_date

                if hour_info:
                    print (hour_info)
                    hour_info['coin_id'] = coin.id
                    CoinHourlyInfo.objects.create(**hour_info)


if __name__ == "__main__":
    main()
