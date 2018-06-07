culture = Culture.objects.filter(name='en_US').first()

for coin in MasterCoin.objects.all():
    cl = CoinLocale.objects.filter(coin=coin, culture=culture).first()
    if not cl:
        full_name = CoinapiCoin.objects.filter(symbol=coin.original_symbol).first()
        if full_name:
            CoinLocale.objects.create(coin=coin, culture=culture, name=full_name.name )

