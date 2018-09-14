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

def get_start_date(coin):
    result = CoinHourlyInfo.objects.filter(coin=coin) \
                                   .order_by('date_of_entry') \
                                   .first()
    return result.date_of_entry.date() if result else date.today()

def main():
    for coin in MasterCoin.objects.all():
        if coin.coingecko:
            hour_info = {}
            data_start_date = get_start_date(coin)

            for single_date in daterange(date(2016, 1, 1), data_start_date):
                try:
                    cg_coin = CoingeckoCoin.objects.get(id=coin.coingecko)
                    url_ = 'https://api.coingecko.com/api/v3/coins/{}/history?date={}&localization=false'.format(cg_coin.uid, single_date.strftime("%d-%m-%Y"))
                    info = requests.get(url_).json()
                    
                    community_data = info.get('community_data', {})
                    developer_data = info.get('developer_data', {})
                    public_interest_stats = info.get('public_interest_stats', {})
                    
                    hour_info['facebook_likes'] = community_data.get('facebook_likes')
                    hour_info['twitter_followers'] = community_data.get('twitter_followers')
                    hour_info['reddit_subscribers'] = community_data.get('reddit_subscribers')
                    hour_info['reddit_average_posts_48h'] = community_data.get('reddit_average_posts_48h')
                    hour_info['reddit_average_comments_48h'] = community_data.get('reddit_average_comments_48h')
                    hour_info['reddit_accounts_active_48h'] = int(float(community_data.get('reddit_accounts_active_48h') or 0))

                    hour_info['repo_forks'] = developer_data.get('forks')
                    hour_info['repo_stars'] = developer_data.get('stars')
                    hour_info['repo_subscribers'] = developer_data.get('subscribers')
                    hour_info['repo_total_issues'] = developer_data.get('total_issues')
                    hour_info['repo_closed_issues'] = developer_data.get('closed_issues')
                    hour_info['repo_pull_requests_merged'] = developer_data.get('pull_requests_merged')
                    hour_info['repo_pull_request_contributors'] = developer_data.get('pull_request_contributors')
                    hour_info['repo_commit_count_4_weeks'] = developer_data.get('commit_count_4_weeks')
                    hour_info['alexa_rank'] = public_interest_stats.get('alexa_rank')
                    hour_info['bing_matches'] = public_interest_stats.get('bing_matches')
                    hour_info['date_of_entry'] = single_date

                    hour_info['coin_id'] = coin.id
                    CoinHourlyInfo.objects.create(**hour_info)
                except Exception as e:
                    print url_
                    print str(e)


if __name__ == "__main__":
    main()
