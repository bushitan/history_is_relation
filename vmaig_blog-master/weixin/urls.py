from django.conf.urls import patterns, include, url

from weixin.views import *

urlpatterns=patterns('',
    url(r'^$','weixin.views.Index'),

)