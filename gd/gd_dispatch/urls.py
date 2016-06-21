# -*- coding: utf-8 -*-
from django.conf.urls import url
from gd_dispatch.views import *

urlpatterns = [
        url(r'^test$', TestView.as_view()),
        url(r'^api/monitor/get_ip$', MonitorGetIP.as_view()),
        url(r'^api/monitor/set_ip$', MonitorSetIP.as_view()),
]