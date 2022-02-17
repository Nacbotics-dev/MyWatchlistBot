"""Vigilis BOT URL Configuration"""

from django.contrib import admin
from django.conf import settings
from django.urls import path,re_path
from Watchlist.views import WebConnect
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.views.static import serve
from MyWatchlist.settings import WEBHOOK_TOKEN


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r''+WEBHOOK_TOKEN,WebConnect,),
    url(r'',WebConnect,),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
