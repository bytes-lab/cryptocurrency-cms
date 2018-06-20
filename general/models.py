from __future__ import unicode_literals

import time
import thread

from django.db import models
from django.db import connection
from django.db.models.signals import post_save

class DataProvider(models.Model):
    provider_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'data_provider'

    def __str__(self):
        return self.provider_code


class Culture(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'culture'

    def __str__(self):
        return self.name


class MasterCoin(models.Model):
    symbol = models.CharField(max_length=255)
    original_symbol = models.CharField(max_length=255)

    coinmarketcap = models.IntegerField(null=True, blank=True)
    cryptocompare = models.IntegerField(null=True, blank=True)
    coingecko = models.IntegerField(null=True, blank=True)
    cryptocompare_name = models.CharField(max_length=255, null=True, blank=True)
    coinapi = models.IntegerField(null=True, blank=True)        # 
    supported_exchanges = models.CharField(max_length=255, null=True, blank=True)
    is_trading = models.BooleanField(default=True)
    sort_order = models.IntegerField(null=True, blank=True)
    image_uri = models.CharField(max_length=255, null=True, blank=True)

    category = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    coingecko_category = models.CharField(max_length=500, null=True, blank=True)
    cmc_tags = models.CharField(max_length=500, null=True, blank=True)

    launch_date = models.DateField(null=True, blank=True)
    proof_type = models.CharField(max_length=255, null=True, blank=True)
    algorithm = models.CharField(max_length=255, null=True, blank=True)

    chat_discord_identifier = models.CharField(max_length=500, null=True, blank=True)
    chat_telegram_identifier = models.CharField(max_length=500, null=True, blank=True)
    chat_slack_identifier = models.CharField(max_length=500, null=True, blank=True)
    social_facebook_identifier = models.CharField(max_length=500, null=True, blank=True)
    social_reddit_identifier = models.CharField(max_length=500, null=True, blank=True)
    social_twitter_identifier = models.CharField(max_length=500, null=True, blank=True)
    social_btt_identifier = models.CharField(max_length=500, null=True, blank=True)
    links_website = models.CharField(max_length=500, null=True, blank=True)
    links_whitepaper = models.CharField(max_length=500, null=True, blank=True)
    links_ann = models.CharField(max_length=500, null=True, blank=True)
    links_explorer = models.CharField(max_length=500, null=True, blank=True)
    links_source_code = models.CharField(max_length=500, null=True, blank=True)
    links_forum = models.CharField(max_length=500, null=True, blank=True)
    links_blog = models.CharField(max_length=500, null=True, blank=True)
    ico_data = models.TextField(null=True, blank=True)

    type_is_crypto = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False)
    supported = models.BooleanField(default=False)
    supported_at = models.DateField(null=True, blank=True)
    alias = models.ForeignKey("MasterCoin", null=True, blank=True)

    class Meta:
        db_table = 'coin'

    def __str__(self):
        return self.symbol


class Exchange(models.Model):
    uid = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)                                     # normalized name
    cryptocompare = models.CharField(max_length=255, null=True, blank=True)     # name on cryptocompare
    coinapi = models.CharField(max_length=255, null=True, blank=True)
    coinmarketcap = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    fees_description = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    twitter_handle = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    reddit_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    api_link = models.CharField(max_length=255, null=True, blank=True)
    script_present = models.BooleanField(default=False)
    supported = models.BooleanField(default=False)
    supported_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'exchange'

    def __str__(self):
        return self.name


class ExchangePair(models.Model):
    exchange = models.ForeignKey(Exchange, related_name="pairs")
    base_coin = models.ForeignKey(MasterCoin, related_name="base_coins")
    quote_coin = models.ForeignKey(MasterCoin, related_name="quote_coins")
    cryptocompare_availability = models.BooleanField(default=False)
    coinapi_availability = models.BooleanField(default=False)
    data_start = models.DateField(null=True, blank=True)
    data_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    raw_trade_source = models.CharField(max_length=255, null=True, blank=True)
    orderbook_source = models.CharField(max_length=255, null=True, blank=True)
    supported = models.BooleanField(default=False)
    supported_at = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'exchange_pair'

    def __str__(self):
        return '{}: {}-{}'.format(self.exchange.name, self.base_coin.symbol, self.quote_coin.symbol)


class ExchangePairXref(models.Model):
    exchange = models.CharField(max_length=255)
    base_coin = models.CharField(max_length=255)
    quote_coin = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    cryptocompare_availability = models.BooleanField(default=False)
    coinapi_availability = models.BooleanField(default=False)

    class Meta:
        db_table = 'exchange_pair_xref'

    def __str__(self):
        return '{}-{}-{}'.format(self.exchange, self.base_coin, self.quote_coin)


class ExchangePairRawTradeProviderXref(models.Model):
    exchange_pair = models.ForeignKey(ExchangePair)
    data_provider_id = models.ForeignKey(DataProvider)
    is_available = models.BooleanField(default=True)
    provider_exch_code = models.CharField(max_length=255)
    provider_base_ccy_code = models.CharField(max_length=255)
    provider_quote_ccy_code = models.CharField(max_length=255)
    market_type = models.CharField(max_length=255)
    source_type = models.IntegerField(default=1)

    class Meta:
        db_table = 'exchange_pair_xreff'


class CryptocompareCoin(models.Model):
    uid = models.IntegerField(null=True)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    coinname = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    image_uri = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'cc_coin_xref'

    def __str__(self):
        return self.symbol


class CoinmarketcapCoin(models.Model):
    token = models.CharField(max_length=255)      # id from api
    symbol = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'cmc_coin_xref'

    def __str__(self):
        return '{} - {}'.format(self.symbol, self.token)


class CoinapiCoin(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'coinapi_coin_xref'

    def __str__(self):
        return self.symbol


class CoingeckoCoin(models.Model):
    uid = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'coingecko_coin_xref'

    def __str__(self):
        return self.symbol


class CoinapiCoin(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'coinapi_coin_xref'

    def __str__(self):
        return self.symbol


class CryptocomparePair(models.Model):
    exchange = models.CharField(max_length=255)
    base_coin = models.CharField(max_length=255)
    quote_coin = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'cc_pair_xref'

    def __str__(self):
        return '{} - {}'.format(self.base_coin, self.quote_coin)


class CoinapiPair(models.Model):
    exchange = models.CharField(max_length=255)
    base_coin = models.CharField(max_length=255)
    quote_coin = models.CharField(max_length=255)
    symbol_id = models.CharField(max_length=255)
    market_type = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'coinapi_pair_xref'

    def __str__(self):
        return '{} - {}'.format(self.base_coin, self.quote_coin)


class TempPair(models.Model):
    pair = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)
    declined = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tmp_pair'
        unique_together = (("pair", "exchange"),)

    def __str__(self):
        return '{} - {}'.format(self.exchange, self.pair)


class CoinHourlyInfo(models.Model):
    coin = models.ForeignKey(MasterCoin)
    date_of_entry = models.DateTimeField(auto_now_add=True)
    total_supply = models.FloatField(null=True)
    circulating_supply = models.FloatField(null=True)
    net_hashes_per_second = models.FloatField(null=True)
    block_time = models.IntegerField(null=True)
    block_reward = models.FloatField(null=True)
    block_number = models.IntegerField(null=True)
    block_reward_reduction = models.CharField(max_length=255, null=True, blank=True)
    difficulty_adjustment = models.CharField(max_length=255, null=True, blank=True)

    facebook_likes = models.IntegerField(null=True)
    twitter_followers = models.IntegerField(null=True)
    reddit_subscribers = models.IntegerField(null=True)
    reddit_average_posts_48h = models.IntegerField(null=True)
    reddit_average_comments_48h = models.IntegerField(null=True)
    reddit_accounts_active_48h = models.IntegerField(null=True)

    repo_forks = models.IntegerField(null=True)
    repo_stars = models.IntegerField(null=True)
    repo_subscribers = models.IntegerField(null=True)
    repo_total_issues = models.IntegerField(null=True)
    repo_closed_issues = models.IntegerField(null=True)
    repo_pull_requests_merged = models.IntegerField(null=True)
    repo_pull_request_contributors = models.IntegerField(null=True)
    repo_commit_count_4_weeks = models.IntegerField(null=True)
    alexa_rank = models.IntegerField(null=True)
    bing_matches = models.IntegerField(null=True)

    class Meta:
        db_table = 'coin_hourly_info'

    def __unicode__(self):
        return self.coin.symbol


class CoinLocale(models.Model):
    coin = models.ForeignKey(MasterCoin)
    culture = models.ForeignKey(Culture)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    feature = models.TextField(null=True, blank=True)
    technology = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'coin_locale'
        unique_together = ('coin', 'culture',)

    def __unicode__(self):
        return u'{} - {}'.format(self.coin.symbol, self.name)


def dictfetchall(cursor, base, quote):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    result = []
    
    for row in cursor.fetchall():
        ii = dict(zip(columns, row))
        ii.pop('base_currency')
        ii.pop('quote_currency')
        ii['base_currency_id'] = base
        ii['quote_currency_id'] = quote
        result.append(ii)
    return result

def support_pair_(instance):
    pair_ = '{}-{}'.format(instance.base_coin.original_symbol, instance.quote_coin.original_symbol)
    # delete a record in temp pair table
    TempPair.objects.filter(exchange=instance.exchange.name, pair=pair_).delete()
    table_name = 'tmp_{}_rates'.format(instance.exchange.name.lower())
    query = "SELECT * FROM {} WHERE base_currency = %s and quote_currency = %s".format(table_name)

    with connection.cursor() as cursor:
        cursor.execute(query, [instance.base_coin.original_symbol, instance.quote_coin.original_symbol])
        res = dictfetchall(cursor, instance.base_coin.id, instance.quote_coin.id)

        if res:
            values = []
            placeholders = ', '.join(['%s'] * len(res[0]))
            columns = ', '.join(res[0].keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON CONFLICT DO NOTHING" % (table_name[4:], columns, placeholders)

            # copy records
            for ii in res:
                values.append(ii.values())
            cursor.executemany(sql, values)

            # delete records in temp table
            query = "DELETE FROM {} WHERE base_currency = %s and quote_currency = %s".format(table_name)
            cursor.execute(query, [instance.base_coin.original_symbol, instance.quote_coin.original_symbol])

def support_pair(sender, instance, **kwargs):
    thread.start_new_thread(support_pair_, (instance,))

post_save.connect(support_pair, sender=ExchangePair)
