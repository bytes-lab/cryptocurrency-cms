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

def get_csv(str1, list2):
    list_val = (str1 or '').split(',') + list2
    list_val = [ii for ii in list_val if ii and ii.strip()]
    return ','.join(set(list_val))

def main():
    for coin in MasterCoin.objects.all():
        hour_info = {}
        locale_info = {}

        if coin.cryptocompare:
            cc_coin = CryptocompareCoin.objects.get(id=coin.cryptocompare)
            url_ = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={}'.format(cc_coin.uid)
            info = requests.get(url_).json()['Data']['General']

            coin.launch_date = datetime.datetime.strptime(info['StartDate'], '%d/%m/%Y') if info.get('StartDate') and info.get('StartDate') != '01/01/0001' else None
            coin.algorithm = info.get('Algorithm')
            coin.proof_type = info.get('ProofType')
            coin.links_website = get_csv(coin.links_website, [info.get('WebsiteUrl')])
            coin.social_twitter_identifier = get_csv(coin.social_twitter_identifier, [info.get('Twitter')])

            hour_info = {
                'total_supply': info.get('TotalCoinSupply'),
                'net_hashes_per_second': info.get('NetHashesPerSecond'),
                'block_number': info.get('BlockNumber'),
                'block_reward_reduction': info.get('BlockRewardReduction'),
                'difficulty_adjustment': info.get('DifficultyAdjustment'),
                'block_time': info.get('BlockTime') or -1,
                'block_reward': info.get('BlockReward')            
            }

            locale_info = {
                'feature': info.get('Features'),
                'technology': info.get('Technology')
            }

        if coin.coingecko:
            cg_coin = CoingeckoCoin.objects.get(id=coin.coingecko)
            url_ = 'https://api.coingecko.com/api/v3/coins/{}'.format(cg_coin.uid)
            info = requests.get(url_).json()

            coin.coingecko_category = get_csv('', info.get('categories'))
            coin.ico_data = json.dump(info.get('ico_data', {}))
            
            coin.chat_telegram_identifier = get_csv(coin.chat_telegram_identifier, [info.get('links')['telegram_channel_identifier']])
            # coin.chat_discord_identifier = get_csv(coin.chat_discord_identifier, info.get('WebsiteUrl'))
            coin.chat_slack_identifier = get_csv(coin.chat_slack_identifier, info.get('ico_data', {}).get('links', {}).get('slack'))

            # coin.social_reddit_identifier = get_csv(coin.social_reddit_identifier, info.get('WebsiteUrl'))
            coin.social_twitter_identifier = get_csv(coin.social_twitter_identifier, [info.get('links')['twitter_screen_name']])
            coin.social_facebook_identifier = info.get('links')['facebook_username']
            coin.social_btt_identifier = info.get('links')['bitcointalk_thread_identifier']
            
            coin.links_website = get_csv(coin.links_website, info.get('links')['homepage'])
            coin.links_whitepaper = get_csv(coin.links_whitepaper, info.get('ico_data', {}).get('links', {}).get('whitepaper'))
            coin.links_ann = get_csv(coin.links_ann, info.get('links')['announcement_url'])
            coin.links_explorer = get_csv(coin.links_explorer, info.get('links')['blockchain_site'])
            coin.links_source_code = get_csv(coin.links_source_code, info.get('ico_data', {}).get('links', {}).get('github'))
            coin.links_forum = get_csv(coin.links_forum, info.get('links')['official_forum_url'])
            coin.links_blog = get_csv(coin.links_blog, info.get('ico_data', {}).get('links', {}).get('blog'))

            # hour_info['circulating_supply'] = info.get('Twitter')
            hour_info['twitter_followers'] = info.get('community_data')['twitter_followers']
            # hour_info['github_commits'] = info.get('Twitter')
            hour_info['reddit_followers'] = info.get('community_data')['reddit_subscribers']

        coin.save()

        if hour_info:
            hour_info['coin_id'] = coin.id
            CoinHourlyInfo.objects.create(**hour_info)

        if locale_info:
            coin.locale_set.first().update(**locale_info)


if __name__ == "__main__":
    main()
