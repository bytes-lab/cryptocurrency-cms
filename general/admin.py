from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from general.models import *


class CoinLocaleTabularInline(admin.TabularInline):
    model = CoinLocale
    extra = 0
    fields = ['name', 'culture', 'short_description', 'description', 'feature', 
              'technology', 'edited']


class CoinEventCategoryLocaleTabularInline(admin.TabularInline):
    model = CoinEventCategoryLocale
    extra = 0
    fields = ['name', 'locale']


class CoinEventLocaleTabularInline(admin.TabularInline):
    model = CoinEventLocale
    extra = 0
    fields = ['culture', 'title', 'status', 'description']


class CryptocompareSupportFilter(SimpleListFilter):
    title = 'cryptocompare'
    parameter_name = 'cryptocompare'

    def lookups(self, request, model_admin):
        return (('Found', 'Found'), 
                ('Not Linked Yet', 'Not Linked Yet'), 
                ('Not Found', 'Not Found'))

    def queryset(self, request, queryset):
        if self.value() == 'Found':
            return queryset.filter(cryptocompare__gt=0)
        if self.value() == 'Not Found':
            return queryset.filter(cryptocompare=0)
        if self.value() == 'Not Linked Yet':
            return queryset.filter(cryptocompare__isnull=True)


class CoinapiSupportFilter(SimpleListFilter):
    title = 'coinapi'
    parameter_name = 'coinapi'

    def lookups(self, request, model_admin):
        return (('Found', 'Found'), 
                ('Not Linked Yet', 'Not Linked Yet'), 
                ('Not Found', 'Not Found'))

    def queryset(self, request, queryset):
        if self.value() == 'Found':
            return queryset.filter(coinapi__gt=0)
        if self.value() == 'Not Found':
            return queryset.filter(coinapi=0)
        if self.value() == 'Not Linked Yet':
            return queryset.filter(coinapi__isnull=True)


class CoinmarketcapSupportFilter(SimpleListFilter):
    title = 'coinmarketcap'
    parameter_name = 'coinmarketcap'

    def lookups(self, request, model_admin):
        return (('Found', 'Found'), 
                ('Not Linked Yet', 'Not Linked Yet'), 
                ('Not Found', 'Not Found'))

    def queryset(self, request, queryset):
        if self.value() == 'Found':
            return queryset.filter(coinmarketcap__gt=0)
        if self.value() == 'Not Found':
            return queryset.filter(coinmarketcap=0)
        if self.value() == 'Not Linked Yet':
            return queryset.filter(coinmarketcap__isnull=True)


class CoinmarketcalSupportFilter(SimpleListFilter):
    title = 'coinmarketcal'
    parameter_name = 'coinmarketcal'

    def lookups(self, request, model_admin):
        return (('Found', 'Found'), 
                ('Not Linked Yet', 'Not Linked Yet'), 
                ('Not Found', 'Not Found'))

    def queryset(self, request, queryset):
        if self.value() == 'Found':
            return queryset.filter(coinmarketcal__gt=0)
        if self.value() == 'Not Found':
            return queryset.filter(coinmarketcal=0)
        if self.value() == 'Not Linked Yet':
            return queryset.filter(coinmarketcal__isnull=True)


class CoingeckoSupportFilter(SimpleListFilter):
    title = 'coingecko'
    parameter_name = 'coingecko'

    def lookups(self, request, model_admin):
        return (('Found', 'Found'), 
                ('Not Linked Yet', 'Not Linked Yet'), 
                ('Not Found', 'Not Found'))

    def queryset(self, request, queryset):
        if self.value() == 'Found':
            return queryset.filter(coingecko__gt=0)
        if self.value() == 'Not Found':
            return queryset.filter(coingecko=0)
        if self.value() == 'Not Linked Yet':
            return queryset.filter(coingecko__isnull=True)


class MasterCoinAdmin(admin.ModelAdmin):
    inlines = [CoinLocaleTabularInline]
    list_display = ['symbol', 'alias', 'cryptocompare_support', 'coinapi_support', 
                    'coinmarketcap_support', 'coingecko_support', 'coinmarketcal_support']
    search_fields = ['symbol']
    list_filter = [CoinmarketcalSupportFilter, CoingeckoSupportFilter, 
                   CoinmarketcapSupportFilter, CoinapiSupportFilter, 
                   CryptocompareSupportFilter, 'supported', 'is_master']

    def cryptocompare_support(self, obj):
        if obj.cryptocompare > 0:
            return 'Found'
        elif obj.cryptocompare == 0:
            return 'Not Found'
        else:
            return 'Not Linked Yet'
    cryptocompare_support.short_description = 'Cryptocompare'

    def coingecko_support(self, obj):
        if obj.coingecko > 0:
            return 'Found'
        elif obj.coingecko == 0:
            return 'Not Found'
        else:
            return 'Not Linked Yet'
    coingecko_support.short_description = 'Coingecko'

    def coinmarketcal_support(self, obj):
        if obj.coinmarketcal > 0:
            return 'Found'
        elif obj.coinmarketcal == 0:
            return 'Not Found'
        else:
            return 'Not Linked Yet'
    coinmarketcal_support.short_description = 'Coinmarketcal'

    def coinapi_support(self, obj):
        if obj.coinapi > 0:
            return 'Found'
        elif obj.coinapi == 0:
            return 'Not Found'
        else:
            return 'Not Linked Yet'
    coinapi_support.short_description = 'Coinapi'

    def coinmarketcap_support(self, obj):
        if obj.coinmarketcap > 0:
            return 'Found'
        elif obj.coinmarketcap == 0:
            return 'Not Found'
        else:
            return 'Not Linked Yet'
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


class GKCoinAdmin(admin.ModelAdmin):
    list_display = ['uid', 'symbol', 'name', 'is_deleted']
    search_fields = ['uid', 'symbol', 'name']
    list_filter = ['is_deleted']


class CMCCoinAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'token']
    search_fields = ['symbol', 'token']


class CoinmarketcalEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_event', 'created_date']
    search_fields = ['title', 'date_event', 'created_date']


class CoinEventAdmin(admin.ModelAdmin):
    inlines = [CoinEventLocaleTabularInline]
    list_display = ['title', 'date_event_start', 'created_date']
    search_fields = ['title', 'date_event_start', 'created_date']


class CoinEventCategoryAdmin(admin.ModelAdmin):
    inlines = [CoinEventCategoryLocaleTabularInline]


class QBTAGGXrefAdmin(admin.ModelAdmin):
    list_display = ['base_coin', 'quote_coin', 'source']
    search_fields = ['base_coin', 'quote_coin', 'source']
    list_filter = ['source']


admin.site.register(MasterCoin, MasterCoinAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(ExchangePair, ExchangePairAdmin)
admin.site.register(DataProvider)
admin.site.register(Culture)
admin.site.register(QBTAGGXref, QBTAGGXrefAdmin)
admin.site.register(CoinEventCategory, CoinEventCategoryAdmin)
admin.site.register(CoinmarketcalCategory)
admin.site.register(CoinmarketcalEvent, CoinmarketcalEventAdmin)
admin.site.register(CoinEvent, CoinEventAdmin)
admin.site.register(CryptocompareCoin, CCCoinAdmin)
admin.site.register(CoinmarketcapCoin, CMCCoinAdmin)
admin.site.register(CoingeckoCoin, GKCoinAdmin)
admin.site.register(CoinmarketcalCoin, GKCoinAdmin)
admin.site.register(CoinapiCoin, CPCoinAdmin)
admin.site.register(CryptocomparePair, ExchangePairXrefAdmin)
admin.site.register(CoinapiPair, ExchangePairXrefAdmin)
admin.site.register(QBTAGGQuote)
