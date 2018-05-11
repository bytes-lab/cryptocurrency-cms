from django.contrib import admin

from general.models import *

class MasterCoinAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'launch_date', 'algorithm', 'cryptocompare', 'is_trading', 'sort_order']
    search_fields = ['symbol', 'algorithm']


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'cryptocompare_support', 'coinapi_support']
    search_fields = ['name']
    list_filter = ['cryptocompare', 'coinapi']

    def cryptocompare_support(self, obj):
        return obj.cryptocompare > 0
    cryptocompare_support.boolean = True

    def coinapi_support(self, obj):
        return obj.coinapi > 0
    coinapi_support.boolean = True


class ExchangePairAdmin(admin.ModelAdmin):
    list_display = ['exchange', 'base_coin', 'quote_coin']
    list_filter = ['exchange']


admin.site.register(MasterCoin, MasterCoinAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(ExchangePair, ExchangePairAdmin)
admin.site.register(DataProvider)
