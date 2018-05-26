import json
import datetime

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from general.models import *


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            message = 'Your login credential is incorrect! Please try again.'
            return render(request, 'login.html', {
                'message': message,
            })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login') 


@login_required(login_url='/login')
def home(request):
    return render(request, 'index.html', {})


@login_required(login_url='/login')
def world_of_coins(request):
    return render(request, 'world_of_coins.html', {})


@login_required(login_url='/login')
def all_coins(request):
    return render(request, 'all_coins.html', {})


@login_required(login_url='/login')
def master_coins(request):
    return render(request, 'master_coins.html', {})


@login_required(login_url='/login')
def exchanges(request):
    return render(request, 'exchanges.html', {})


@login_required(login_url='/login')
def supported_exchanges(request):
    return render(request, 'supported_exchanges.html', {})


@login_required(login_url='/login')
def exchange_detail(request, id):
    exchange = Exchange.objects.get(id=id)
    return render(request, 'exchange_detail.html', { "exchange": exchange })


@login_required(login_url='/login')
def exchange_support(request, id):
    exchange = Exchange.objects.get(id=id)
    exchange.supported = True
    exchange.supported_at = datetime.datetime.now()
    exchange.save()
    return HttpResponseRedirect(reverse('exchange_detail', kwargs={ 'id': id }))

@login_required(login_url='/login')
def add_pair(request, exchange, pair):
    [base, quote] = pair.split('-')
    exchange = Exchange.objects.get(id=exchange)
    # pair.supported = True
    # pair.supported_at = datetime.datetime.now()
    # pair.save()
    return HttpResponseRedirect(reverse('exchange_detail', kwargs={ 'id': exchange.id }))

@login_required(login_url='/login')
def add_coin(request, coin, exchange):
    exchange = Exchange.objects.get(id=exchange)
    cc_pairs = CryptocomparePair.objects.filter(Q(exchange__iexact=exchange.cryptocompare) & (Q(base_coin=coin)|Q(quote_coin=coin)))
    cp_pairs = CoinapiPair.objects.filter(Q(exchange__iexact=exchange.coinapi) & (Q(base_coin=coin)|Q(quote_coin=coin)))

    cc_coins = CryptocompareCoin.objects.all()
    cmc_coins = CoinmarketcapCoin.objects.all()
    cp_coins = CoinapiCoin.objects.all()

    coin__ = coin.replace('*', '')
    ccd_coins = [ii.symbol for ii in CryptocompareCoin.objects.filter(symbol__startswith=coin__)]
    ccd_coins = ', '.join(ccd_coins) if len(ccd_coins) > 1 else ''
    cmcd_coins = [ii.symbol for ii in CoinmarketcapCoin.objects.filter(symbol__startswith=coin__)]
    cmcd_coins = ', '.join(cmcd_coins) if len(cmcd_coins) > 1 else ''
    cpd_coins = [ii.symbol for ii in CoinapiCoin.objects.filter(symbol__startswith=coin__)]
    cpd_coins = ', '.join(cpd_coins) if len(cpd_coins) > 1 else ''

    if request.method == 'POST':
        cc = request.POST.get('cc_coin') or None
        cmc = request.POST.get('cmc_coin') or None
        cp = request.POST.get('cp_coin') or None
        cc_name = CryptocompareCoin.objects.get(id=cc).name if cc else ''
        coin = MasterCoin(cryptocompare=cc,
                          coinmarketcap=cmc,
                          coinapi=cp,
                          cryptocompare_name=cc_name,
                          symbol=coin,
                          supported=True,
                          is_master=True,
                          is_trading=True)
        coin.save()
        coin = MasterCoin.objects.get(id=coin.id) # weird

    return render(request, 'add_coin.html', locals())

@login_required(login_url='/login')
def attach_coin(request, coin):
    coin = MasterCoin.objects.get(id=coin)
    cc_coins = CryptocompareCoin.objects.all()
    cmc_coins = CoinmarketcapCoin.objects.all()
    cp_coins = CoinapiCoin.objects.all()

    coin__ = coin.symbol.replace('*', '')
    ccd_coins = [ii.symbol for ii in CryptocompareCoin.objects.filter(symbol__startswith=coin__)]
    ccd_coins = ', '.join(ccd_coins) if len(ccd_coins) > 1 else ''
    cmcd_coins = [ii.symbol for ii in CoinmarketcapCoin.objects.filter(symbol__startswith=coin__)]
    cmcd_coins = ', '.join(cmcd_coins) if len(cmcd_coins) > 1 else ''
    cpd_coins = [ii.symbol for ii in CoinapiCoin.objects.filter(symbol__startswith=coin__)]
    cpd_coins = ', '.join(cpd_coins) if len(cpd_coins) > 1 else ''

    if request.method == 'POST':
        coin.cryptocompare = request.POST.get('cc_coin') or None
        coin.coinmarketcap = request.POST.get('cmc_coin') or None
        coin.coinapi = request.POST.get('cp_coin') or None
        if coin.cryptocompare:
            coin.cryptocompare_name = CryptocompareCoin.objects.get(id=coin.cryptocompare).name
        coin.save()
        coin = MasterCoin.objects.get(id=coin.id) # weird

    return render(request, 'add_coin.html', locals())

@login_required(login_url='/login')
def add_to_world(request, id):
    coin = MasterCoin.objects.get(id=id)
    coin.supported = True
    coin.save()
    return HttpResponseRedirect(reverse('all_coins'))


@login_required(login_url='/login')
def import_all_pairs(request, id):
    exchange = Exchange.objects.get(id=id)
    exchange.pairs.update(supported=True)
    exchange.pairs.update(supported_at=datetime.datetime.now())
    # support base coin of pairs
    for pair in exchange.pairs.all():
        pair.base_coin.supported = True
        pair.base_coin.supported_at = datetime.datetime.now()
        pair.base_coin.save()
    return HttpResponseRedirect(reverse('exchange_detail', kwargs={ 'id': id }))


@csrf_exempt
def coins_(request):
    q = Q(is_master=True)
    return _coins(request, q)

@csrf_exempt
def supported_coins_(request):
    q = Q(supported=True)
    return _coins(request, q)

@csrf_exempt
def all_coins_(request):
    q = Q()
    return _coins(request, q)

def _coins(request, q):
    limit = int(request.POST.get('rowCount'))
    page = int(request.POST.get('current'))
    keyword = request.POST.get('searchPhrase')

    qs = MasterCoin.objects.filter(q & Q(symbol__icontains=keyword))
    total = qs.count()
    coins = []

    cc_coins = [ii.symbol for ii in CryptocompareCoin.objects.all()]
    cmc_coins = [ii.symbol for ii in CoinmarketcapCoin.objects.all()]
    cp_coins = [ii.symbol for ii in CoinapiCoin.objects.all()]

    lstart = (page - 1) * limit
    lend = lstart + limit

    for coin in qs[lstart:lend]:
        status = 'SUPPORTED' if coin.supported else 'On World of Coins' if coin.is_master else 'NEW'
        coin_ = {
            'id': coin.id,
            'symbol': coin.symbol,
            'cryptocompare': 'YES' if coin.cryptocompare > 0 else 'NO',
            'coinapi': 'YES' if coin.coinapi > 0  else 'NO',
            'cmc': 'YES' if coin.coinmarketcap > 0 else 'NO',
            'supported': 'YES' if coin.supported else 'NO',
            'status': status
        }
        coins.append(coin_)

    return JsonResponse({
        "current": page,
        "rowCount": limit,
        "rows": coins,
        "total": total
        }, safe=False)

@csrf_exempt
def exchanges_(request):
    limit = int(request.POST.get('rowCount'))
    page = int(request.POST.get('current'))
    keyword = request.POST.get('searchPhrase')

    qs = Exchange.objects.filter(name__icontains=keyword)
    total = qs.count()
    exchanges = []

    lstart = (page - 1) * limit
    lend = lstart + limit

    for exchange in qs[lstart:lend]:
        exchange_ = {
            'id': exchange.id,
            'name': exchange.name,
            'cryptocompare': 'YES' if exchange.cryptocompare > 0 else 'NO',
            'coinapi': 'YES' if exchange.coinapi > 0 else 'NO',
            'supported': 'YES' if exchange.supported else 'NO'
        }
        exchanges.append(exchange_)

    return JsonResponse({
        "current": page,
        "rowCount": limit,
        "rows": exchanges,
        "total": total
        }, safe=False)


@csrf_exempt
def supported_exchanges_(request):
    limit = int(request.POST.get('rowCount'))
    page = int(request.POST.get('current'))
    keyword = request.POST.get('searchPhrase')

    qs = Exchange.objects.filter(name__icontains=keyword, supported=True)
    total = qs.count()
    exchanges = []

    lstart = (page - 1) * limit
    lend = lstart + limit

    for exchange in qs[lstart:lend]:
        pairs = exchange.pairs.filter(supported=True)
        coins = [pair.base_coin.symbol for pair in pairs if pair.base_coin.supported]

        exchange_ = {
            'id': exchange.id,
            'exchange': exchange.name,
            'num_coins': len(set(coins)),
            'num_pairs': pairs.count()
        }
        exchanges.append(exchange_)

    return JsonResponse({
        "current": page,
        "rowCount": limit,
        "rows": exchanges,
        "total": total
        }, safe=False)


@csrf_exempt
def exchange_detail_(request, id):
    limit = int(request.POST.get('rowCount'))
    page = int(request.POST.get('current'))
    keyword = request.POST.get('searchPhrase')
    lstart = (page - 1) * limit
    lend = lstart + limit

    exchange = Exchange.objects.get(id=id)
    qs = exchange.pairs.filter(Q(base_coin__symbol__icontains=keyword) 
                             | Q(quote_coin__symbol__icontains=keyword)) \
                       .order_by('base_coin')
    result = {}
    for ii in qs:
        is_master = 'Master'
        if ii.base_coin.cryptocompare > 0 and ii.base_coin.coinapi > 0:
            is_master = 'Coinapi / Cryptocompare'
        elif ii.base_coin.cryptocompare > 0:
            is_master = 'Cryptocompare'
        else:
            is_master = 'Coinapi'

        pair = ii.base_coin.symbol + ' / ' + ii.quote_coin.symbol
        result[pair] = {
            'pair': pair,
            'supported': 'YES',
            'coin_supported': True,
            'is_master': is_master,
            'supported_at': str(ii.supported_at) if ii.supported_at else ''
        }

    qs_cc = CryptocomparePair.objects.filter(Q(exchange__iexact=exchange.cryptocompare) &
                                             (Q(base_coin__icontains=keyword) |
                                              Q(quote_coin__icontains=keyword))) \
                                     .order_by('base_coin')

    qs_cp = CoinapiPair.objects.filter(Q(exchange__iexact=exchange.coinapi) &
                                       (Q(base_coin__icontains=keyword) |
                                        Q(quote_coin__icontains=keyword))) \
                               .order_by('base_coin')

    for ii in qs_cc:
        pair = ii.base_coin + ' / ' + ii.quote_coin
        if pair not in result:
            result[pair] = {
                'pair': pair,
                'supported': 'NO',
                'is_master': 'Cryptocompare',
                'supported_at': ''
            }

    for ii in qs_cp:
        pair = ii.base_coin + ' / ' + ii.quote_coin
        if pair in result:
            if result[pair]['supported'] == 'NO':
                result[pair]['is_master'] = 'Coinapi / Cryptocompare'
        else:
            result[pair] = {
                'pair': pair,
                'supported': 'NO',
                'is_master': 'Coinapi',
                'supported_at': ''
            }

    result_cc = []
    for k, v in sorted(result.items()):
        result_cc.append(v)

    pre_coin = None
    for ii in result_cc[lstart:lend]:
        [base, quote] = ii['pair'].split(' / ')
        coin = '' if pre_coin == base else base
        ii['coin'] = coin
        ii['quote_coin'] = quote
        ii['exchange'] = id
        pre_coin = base
        ii['quote_coin_supported'] = MasterCoin.objects.filter(symbol=quote).exists()
        if 'coin_supported' not in ii:
            ii['coin_supported'] = MasterCoin.objects.filter(symbol=base).exists()


    return JsonResponse({
        "current": page,
        "rowCount": limit,
        "rows": result_cc[lstart:lend],
        "total": len(result_cc)
    }, safe=False)
