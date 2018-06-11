from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from general.models import *


class CoinLocaleTabularInline(admin.TabularInline):
    model = CoinLocale
    extra = 0
    fields = ['name', 'culture', 'description']


class CryptocompareSupportFilter(SimpleListFilter):
    title = 'cryptocompare'
    parameter_name = 'cryptocompare'

    def lookups(self, request, model_admin):
        return (('True', _('Yes')), ('False', _('No')))

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(cryptocompare__gt=0)
        if self.value() == 'False':
            return queryset.exclude(cryptocompare__gt=0)


class CoinapiSupportFilter(SimpleListFilter):
    title = 'coinapi'
    parameter_name = 'coinapi'

    def lookups(self, request, model_admin):
        return (('True', _('Yes')), ('False', _('No')))

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(coinapi__gt=0)
        if self.value() == 'False':
            return queryset.exclude(coinapi__gt=0)


class CoinmarketcapSupportFilter(SimpleListFilter):
    title = 'coinmarketcap'
    parameter_name = 'coinmarketcap'

    def lookups(self, request, model_admin):
        return (('True', _('Yes')), ('False', _('No')))

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(coinmarketcap__gt=0)
        if self.value() == 'False':
            return queryset.exclude(coinmarketcap__gt=0)


class MasterCoinAdmin(admin.ModelAdmin):
    inlines = [CoinLocaleTabularInline]
    list_display = ['symbol', 'alias', 'cryptocompare_support', 'coinapi_support', 'coinmarketcap_support']
    search_fields = ['symbol']
    list_filter = [CoinmarketcapSupportFilter, CoinapiSupportFilter, CryptocompareSupportFilter, 'supported', 'is_master']

    def cryptocompare_support(self, obj):
        return obj.cryptocompare > 0
    cryptocompare_support.boolean = True
    cryptocompare_support.short_description = 'Cryptocompare'

    def coinapi_support(self, obj):
        return obj.coinapi > 0
    coinapi_support.boolean = True
    coinapi_support.short_description = 'Coinapi'

    def coinmarketcap_support(self, obj):
        return obj.coinmarketcap > 0
    coinmarketcap_support.boolean = True
    coinmarketcap_support.short_description = 'Coinmarketcap'


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'coinapi_support', 'cryptocompare_support']
    search_fields = ['name']
    list_filter = [CryptocompareSupportFilter, CoinapiSupportFilter]

    def cryptocompare_support(self, obj):
        return obj.cryptocompare != None and obj.cryptocompare.strip() != ''
    cryptocompare_support.boolean = True

    def coinapi_support(self, obj):
        return obj.coinapi != None and obj.coinapi.strip() != ''
    coinapi_support.boolean = True


class ExchangePairAdmin(admin.ModelAdmin):
    list_display = ['exchange', 'base_coin', 'quote_coin', 'supported_at']
    list_filter = ['exchange']


class ExchangePairXrefAdmin(admin.ModelAdmin):
    list_display = ['exchange', 'base_coin', 'quote_coin']
    search_fields = ['exchange', 'base_coin', 'quote_coin']


class CCCoinAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'coinname', 'fullname']
    search_fields = ['symbol', 'name', 'coinname', 'fullname']


class CPCoinAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name']
    search_fields = ['symbol', 'name']


class CMCCoinAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'token']
    search_fields = ['symbol', 'token']


admin.site.register(MasterCoin, MasterCoinAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(ExchangePair, ExchangePairAdmin)
admin.site.register(DataProvider)
admin.site.register(Culture)
# admin.site.register(CoinLocale)
admin.site.register(CryptocompareCoin, CCCoinAdmin)
admin.site.register(CoinmarketcapCoin, CMCCoinAdmin)
admin.site.register(CoinapiCoin, CPCoinAdmin)
admin.site.register(CryptocomparePair, ExchangePairXrefAdmin)
admin.site.register(CoinapiPair, ExchangePairXrefAdmin)
