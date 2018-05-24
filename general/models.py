from __future__ import unicode_literals

from django.db import models


class DataProvider(models.Model):
    provider_code = models.CharField(max_length=255)

    def __str__(self):
        return self.provider_code


class MasterCoin(models.Model):
    symbol = models.CharField(max_length=255)
    coinmarketcap = models.IntegerField(null=True, blank=True)  # (rank in cmc) flag for supporting, assume symbols are same
    cryptocompare = models.IntegerField(null=True, blank=True)  # (symbol id)
    cryptocompare_name = models.CharField(max_length=255, null=True, blank=True)
    coinapi = models.IntegerField(null=True, blank=True)        # 
    supported_exchanges = models.CharField(max_length=255, null=True, blank=True)
    is_trading = models.BooleanField(default=True)
    sort_order = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    whitepaper_url = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    nethash_per_second = models.CharField(max_length=255, null=True, blank=True)
    block_time = models.IntegerField(null=True, blank=True)
    block_reward = models.CharField(max_length=255, null=True, blank=True)
    proof_type = models.CharField(max_length=255, null=True, blank=True)
    algorithm = models.CharField(max_length=255, null=True, blank=True)
    ico_price = models.CharField(max_length=255, null=True, blank=True)
    twitter_handle = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    source_code_url = models.CharField(max_length=255, null=True, blank=True)
    explorers_url = models.CharField(max_length=255, null=True, blank=True)
    slack_channel = models.CharField(max_length=255, null=True, blank=True)
    reddit_url = models.CharField(max_length=255, null=True, blank=True)
    type_is_crypto = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False)
    supported = models.BooleanField(default=False)
    supported_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'mastercoin'

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
    coinmarketcap_availability = models.BooleanField(default=False)
    cryptocompare_availability = models.BooleanField(default=False)
    coinapi_availability = models.BooleanField(default=False)
    data_start = models.DateField(null=True, blank=True)
    data_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    raw_trade_source = models.ForeignKey(MasterCoin, null=True, blank=True, related_name="raw_trade_sources")
    orderbook_source = models.ForeignKey(MasterCoin, null=True, blank=True, related_name="orderbook_sources")
    supported = models.BooleanField(default=False)
    supported_at = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'exchange_pair'

    def __str__(self):
        return '{}: {}-{}'.format(self.exchange.name, self.base_coin.symbol, self.quote_coin.symbol)


class ExchangePairRawTradeProviderXref(models.Model):
    exchange_pair = models.ForeignKey(ExchangePair)
    data_provider_id = models.ForeignKey(DataProvider)
    is_available = models.BooleanField(default=True)
    provider_exch_code = models.CharField(max_length=255)
    provider_base_ccy_code = models.CharField(max_length=255)
    provider_quote_ccy_code = models.CharField(max_length=255)
    source_type = models.IntegerField(default=1)

    class Meta:
        db_table = 'exchange_pair_xref'


class CryptocompareCoin(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'cc_coin_xref'

    def __str__(self):
        return self.symbol


class CoinmarketcapCoin(models.Model):
    token = models.CharField(max_length=255)      # id from api
    symbol = models.CharField(max_length=255)

    class Meta:
        db_table = 'cmc_coin_xref'

    def __str__(self):
        return '{} - {}'.format(self.symbol, self.token)


class CoinapiCoin(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'coinapi_coin_xref'

    def __str__(self):
        return self.symbol


class CryptocomparePair(models.Model):
    exchange = models.CharField(max_length=255)
    base_coin = models.CharField(max_length=255)
    quote_coin = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'cc_pair_xref'

    def __str__(self):
        return '{} - {}'.format(self.base_coin, self.quote_coin)


class CoinapiPair(models.Model):
    exchange = models.CharField(max_length=255)
    base_coin = models.CharField(max_length=255)
    quote_coin = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'coinapi_pair_xref'

    def __str__(self):
        return '{} - {}'.format(self.base_coin, self.quote_coin)
