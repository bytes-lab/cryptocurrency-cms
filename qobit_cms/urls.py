"""qobit_cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from general.views import *

admin.site.site_header = "QOBIT CMS"

urlpatterns = [
	url(r'^jet/', include('jet.urls', 'jet')),
	url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),

    url(r"^login", user_login, name="login"),
    url(r"^logout", user_logout, name="logout"),

    url(r"^$", home, name="home"),
    url(r"^events$", events, name="events"),
    url(r"^events_$", events_, name="events_"),
    url(r"^master_coins$", master_coins, name="master_coins"),
    url(r"^supported_coins_$", supported_coins_, name="supported_coins_"),
    url(r"^exchanges$", exchanges, name="exchanges"),
    url(r"^exchanges_$", exchanges_, name="exchanges_"),
    url(r"^supported_exchanges$", supported_exchanges, name="supported_exchanges"),
    url(r"^supported_exchanges_$", supported_exchanges_, name="supported_exchanges_"),
    url(r"^exchanges/(?P<id>\d+)", exchange_detail, name="exchange_detail"),
    url(r"^exchanges_/(?P<id>\d+)", exchange_detail_, name="exchange_detail_"),
    url(r"^exchange_support/(?P<id>\d+)", exchange_support, name="exchange_support"),
    url(r"^import_all_pairs/(?P<id>\d+)", import_all_pairs, name="import_all_pairs"),
    url(r"^add_pair/(?P<exchange>\d+)/(?P<pair>.+)", add_pair, name="add_pair"),
    url(r"^add_coin/(?P<coin>.+)/(?P<exchange>\d+)", add_coin, name="add_coin"),
    url(r"^attach_coin/(?P<coin>\d+)", attach_coin, name="attach_coin"),
    url(r"^download_icon/(?P<id>\d+)", download_icon, name="download_icon"),
    url(r"^bulk_pair_coin", bulk_pair_coin, name="bulk_pair_coin"),

    url(r"^get_csv", get_csv, name="get_csv"),
    url(r"^get_pairs_info", get_pairs_info, name="get_pairs_info"),
]
