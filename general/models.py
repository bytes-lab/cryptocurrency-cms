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
    sort_order = models.IntegerField()
    image_uri = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)


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
