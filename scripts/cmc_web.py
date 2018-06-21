import json
import time
import requests
import datetime
import urllib2
from lxml import etree

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

def get_urls(lis, txt):
    result = []
    for li in lis:
        text = li.xpath('./a/text()')
        if text and txt in text[0]:
            result = result + li.xpath('./a/@href')
    return result

def get_tags(lis):
    result = []
    for li in lis:
        text = li.xpath('./span[contains(@class, "label label-warning")]/text()')
        result = result + text
    return ','.join(result)

def get_identifier(list1, list2):
    result = []
    for ii in list1:
        if not ii:
            continue
        for iii in list2:
            if iii in ii:
                result.append(ii.split(iii)[1].strip('/'))
    return result

def clean_text(text):
    try:
        return int(text.strip().replace(',', ''))
    except Exception as e:
        pass

def main():
    for coin in MasterCoin.objects.all():
        if coin.coinmarketcap:
            cmc_coin = CoinmarketcapCoin.objects.get(id=coin.coinmarketcap)
            try:
                url_ = 'https://coinmarketcap.com/currencies/{}/'.format(cmc_coin.token)
                response = urllib2.urlopen(url_)
                htmlparser = etree.HTMLParser()
                tree = etree.parse(response, htmlparser)
                xpath = "/html/body/div[@class='container main-section']/div[@class='row']/div[@class='col-lg-10']/div[@class='row bottom-margin-2x']/div[@class='col-sm-4 col-sm-pull-8']/ul[@class='list-unstyled']/li"
                lis = tree.xpath(xpath)
                chats = get_urls(lis, 'Chat')
                coin.chat_discord_identifier = get_csv(coin.chat_discord_identifier, get_identifier(chats, ['discord.gg', 'discordapp.com/invite']))
                coin.chat_telegram_identifier = get_csv(coin.chat_telegram_identifier, get_identifier(chats, ['t.me']))
                coin.cmc_tags = get_tags(lis)
                max_supply = tree.xpath("/html/body/div[@class='container main-section']/div[@class='row']/div[@class='col-lg-10']/div[@class='row bottom-margin-2x']/div[@class='col-sm-8 col-sm-push-4']/div[@class='coin-summary-item col-xs-6  col-md-3 ']/div[@class='coin-summary-item-detail details-text-medium']/span/text()") or tree.xpath("/html/body/div[@class='container main-section']/div[@class='row']/div[@class='col-lg-10']/div[@class='row bottom-margin-2x']/div[@class='col-sm-8 col-sm-push-4']/div[@class='coin-summary-item col-xs-6 col-md-3 col-xs-offset-6 col-md-offset-9']/div[@class='coin-summary-item-detail details-text-medium']/span/text()")
                coin.max_supply = clean_text(max_supply) if max_supply else None
                coin.save()
            except Exception as e:
                print str(e)
                print '---------------------------------'
            print url_


if __name__ == "__main__":
    main()
