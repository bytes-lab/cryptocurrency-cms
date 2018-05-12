import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

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
def exchanges(request):
    return render(request, 'exchanges.html', {})


@csrf_exempt
def coins_(request):
    form_param = json.loads(request.body or "{}")
    limit = int(form_param.get('rowCount'))
    page = int(form_param.get('current'))

    qs = MasterCoin.objects.all()
    total = qs.count()
    coins = []

    lstart = (page - 1) * limit
    lend = lstart + limit

    for coin in qs[lstart:lend]:
        coin_ = {
            'id': coin.id,
            'symbol': coin.symbol,
            'cryptocompare': 'YES' if coin.cryptocompare > 0 else 'NO',
            'coinapi': 'YES' if coin.coinapi > 0 else 'NO',
            'supported': 'YES' if coin.supported else 'NO'
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
    form_param = json.loads(request.body or "{}")
    limit = int(form_param.get('rowCount'))
    page = int(form_param.get('current'))

    qs = Exchange.objects.all()
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