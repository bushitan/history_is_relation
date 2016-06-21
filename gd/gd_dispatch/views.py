# -*- coding: utf-8 -*-
from django.shortcuts import render

from django import template
from django import forms
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import Context, loader
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
# from blog.models import Article, Category, Carousel, Column, Nav, News
# from blog.models import *
from gd_dispatch.models import *
import datetime
import time
import json
import logging

# Create your views here.

class BaseMixin(object):


    def get_context_data(self, *args, **kwargs):


        user = self.request.user
        if not user.is_authenticated():
           kwargs['user_id'] = "none"
        else:
           kwargs['user_id'] = user

        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            a = 5
            # # 热门文章
            # context['hot_article_list'] = \
            #     Article.objects.order_by("-view_times")[0:10]
            # # 导航条
            # context['nav_list'] = Nav.objects.filter(status=0)
            # # 最新评论
            # context['latest_comment_list'] = \
            #     Comment.objects.order_by("-create_time")[0:10]
        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context

class TestView(BaseMixin, ListView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        return super(TestView, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass

class MonitorGetIP(BaseMixin, ListView):
    # template_name = 'time/test1.html'
    def post(self, request, *args, **kwargs):
        _stbsn = self.request.POST.get("stb_sn", "")

        print "OK",_stbsn
        # if RelMonitor.objects.filter(stbsn=_stbsn).exists():
        if STB.objects.filter(sn=_stbsn).exists():
            print "OK1"
            _stb = STB.objects.get(sn=_stbsn)#获取stb
            print "stb",_stb
            _monitor = RelMonitor.objects.filter(stb=_stb)#获取监控关系列表
            # print "Monitor",_m[0].camera.name
            # print _m[1].name,_m[1].sn,_m[0]
            # print _m[0]

            _cameraList = []
            for _m in _monitor:
                _cameraList.append({
                    "name":_m.camera.name,
                    "ip":_m.camera.ip})

            _dict = {
                'style':u"监控",
                'user':_stb.name,
                'cameras': _cameraList
            }
            print _dict
            return HttpResponse(
                json.dumps(_dict),
                content_type="application/json"
            )

        return HttpResponse(u"机顶盒序列号不存在！")

    def get_context_data(self, **kwargs):
        return super(MonitorGetIP, self).get_context_data(**kwargs)

    def get_queryset(self):
        pass

class MonitorSetIP(BaseMixin, ListView):
    # template_name = 'time/test1.html'
    def post(self, request, *args, **kwargs):
        _camera_sn = self.request.POST.get("camera_sn", "")
        _ip = self.request.POST.get("ip", "")
        if Camera.objects.filter(sn=_camera_sn).exists():

            _camera = Camera.objects.get(sn=_camera_sn)
            _camera.ip = _ip
             # print "21"
            _camera.save()
            _word = u"摄像头IP修改成功:"+ _ip
            return HttpResponse(_word)
        return HttpResponse(u"摄像头序列号不存在")
    def get_context_data(self, **kwargs):
        return super(MonitorSetIP, self).get_context_data(**kwargs)

    def get_queryset(self):
        pass