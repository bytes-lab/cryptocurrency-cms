from __future__ import unicode_literals

from django.db import models

class MasterCoin(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    coinmarketcap_slug = models.CharField(max_length=255, null=True, blank=True)
    coinmarketcap = models.IntegerField(null=True, blank=True)
    cryptocompare = models.IntegerField(null=True, blank=True)
    coinapi = models.IntegerField(null=True, blank=True)
    supported_exchanges = models.CharField(max_length=255, null=True, blank=True)
    is_trading = models.BooleanField(default=True)
    sort_order = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    whitepaper_url = models.CharField(max_length=255, null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    nethashespersecond = models.CharField(max_length=255, null=True, blank=True)
    blocktime = models.IntegerField(null=True, blank=True)
    blockreward = models.CharField(max_length=255, null=True, blank=True)
    prooftype = models.CharField(max_length=255, null=True, blank=True)
    algorithm = models.CharField(max_length=255, null=True, blank=True)
    ico_price = models.CharField(max_length=255, null=True, blank=True)
    gains_loss_on_ico_price = models.CharField(max_length=255, null=True, blank=True)
    total_supply = models.CharField(max_length=255, null=True, blank=True)
    circulating_supply = models.CharField(max_length=255, null=True, blank=True)
    market_cap = models.CharField(max_length=255, null=True, blank=True)
    twitter_handle = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_followers = models.IntegerField(default=-1)
    twitter_announcements = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    source_code_url = models.CharField(max_length=255, null=True, blank=True)
    explorers_url = models.CharField(max_length=255, null=True, blank=True)
    github_commits = models.IntegerField(default=-1)
    github_development_tracking = models.CharField(max_length=255, null=True, blank=True)
    slack_channel = models.CharField(max_length=255, null=True, blank=True)
    reddit_url = models.CharField(max_length=255, null=True, blank=True)
    reddit_followers = models.IntegerField(default=-1)

    def __str__(self):
        return self.symbol


class Exchange(models.Model):
    uid = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    cryptocompare = models.IntegerField(null=True, blank=True)
    coinapi = models.IntegerField(null=True, blank=True)
    coinmarketcap = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    fees_description = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    twitter_handle = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    reddit_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ExchangePair(models.Model):
    exchange = models.ForeignKey(Exchange, null=True, blank=True, related_name="exchanges")
    base_coin = models.ForeignKey(MasterCoin, null=True, blank=True, related_name="base_coins")
    quote_coin = models.ForeignKey(MasterCoin, null=True, blank=True, related_name="quote_coins")
    coinmarketcap_availability = models.BooleanField(default=False)
    cryptocompare_availability = models.BooleanField(default=False)
    coinapi_availability = models.BooleanField(default=False)
    data_start = models.DateField(null=True, blank=True)
    data_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{}: {}-{}'.format(self.exchange.name, self.base_coin.symbol, self.quote_coin.symbol)

    class Meta:
        verbose_name = 'Cryptocompare Pair'


class CryptocompareCoin(MasterCoin):
    total_coins_mined = models.IntegerField(null=True, blank=True)


class CryptocompareExchange(Exchange):
    total_coins_mined = models.IntegerField(null=True, blank=True)


class CoinapiPair(ExchangePair):
    symbol_type = models.CharField(max_length=255, null=True, blank=True)


class CoinapiCoin(MasterCoin):
    type_is_crypto = models.BooleanField()


class CoinapiExchange(Exchange):
    company = models.CharField(max_length=255, null=True, blank=True)
    data_start = models.DateField(null=True, blank=True)
    data_end = models.DateField(null=True, blank=True)
    data_quote_start = models.DateTimeField(null=True, blank=True)
    data_quote_end = models.DateTimeField(null=True, blank=True)
    data_orderbook_start = models.DateTimeField(null=True, blank=True)
    data_orderbook_end = models.DateTimeField(null=True, blank=True)
    data_trade_start = models.DateTimeField(null=True, blank=True)
    data_trade_end = models.DateTimeField(null=True, blank=True)
    data_trade_count = models.IntegerField(null=True, blank=True)
    data_symbols_count = models.IntegerField(null=True, blank=True)
