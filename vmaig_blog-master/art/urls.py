# -*- coding: utf-8 -*-

from django.conf.urls import url
from art.views import *
urlpatterns = [

    url(r'^art/main$', MainView.as_view()),
   url(r'^art/pixel_tool$', PixelToolView.as_view()),

]