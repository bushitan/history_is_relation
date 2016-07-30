# -*- coding: utf-8 -*-

from django.conf.urls import url
from art.views import *
from django.views.generic import RedirectView
urlpatterns = [

   url(r'^art/main$', MainView.as_view()),
   url(r'^art/pixel_tool$', PixelToolView.as_view()),
   url(r'^art/pixel_tool/(?P<filename>\w+)$', PixelToolView.as_view()),
   url(r'^art/upload$', UploadView.as_view()),

   url(r'^art/creation$', CreationImgView.as_view()),


   url(r'^art/img_str$', ImgToStrView.as_view()),
   url(r'^art/wx_img_str$', WXImgToStr.as_view()),


   url(r'^art/show/$', ShowView.as_view()),
   url(r'^art/gallery/(?P<openid>\w+)$',GalleryView.as_view()),
   # RedirectView.as_view(url='http://120.27.97.33:82/blog/gallery/11'+)
]