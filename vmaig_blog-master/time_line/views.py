# -*- coding: utf-8 -*-
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
from blog.models import Article, Category, Carousel, Column, Nav, News
from vmaig_comments.models import Comment
from vmaig_auth.models import VmaigUser
from vmaig_auth.forms import VmaigUserCreationForm, VmaigPasswordRestForm
from vmaig_blog.settings import PAGE_NUM
import datetime
import time
import json
import logging

# 缓存
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

logger = logging.getLogger(__name__)




class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 热门文章
            context['hot_article_list'] = \
                Article.objects.order_by("-view_times")[0:10]
            # 导航条
            context['nav_list'] = Nav.objects.filter(status=0)
            # 最新评论
            context['latest_comment_list'] = \
                Comment.objects.order_by("-create_time")[0:10]
        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context

class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM  # 分页--每页的数目

    def get_context_data(self, **kwargs):
        # 轮播
        kwargs['carousel_page_list'] = Carousel.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)
        return article_list







