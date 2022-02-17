"""Vigilis BOT URL Configuration"""

from django.contrib import admin

from django.urls import path
from Watchlist.views import WebConnect
from django.conf.urls import url,include
from MyWatchlist.settings import WEBHOOK_TOKEN


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r''+WEBHOOK_TOKEN,WebConnect,),
    url(r'',WebConnect,),
]
