# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from art.models import *
from vmaig_comments.models import Comment
from vmaig_auth.models import VmaigUser
from vmaig_auth.forms import VmaigUserCreationForm, VmaigPasswordRestForm
from vmaig_blog.settings import PAGE_NUM
from django.views.generic import View, TemplateView, ListView, DetailView
from art.lib.str2img import Str2Img
import datetime
import time
import json
import logging
import os
import base64
from PIL import Image
# logger
logger = logging.getLogger(__name__)


class BaseMixin(object):


    def get_context_data(self, *args, **kwargs):


        user = self.request.user
        if not user.is_authenticated():
           kwargs['user_id'] = "none"
        else:
           kwargs['user_id'] = user


        context = super(BaseMixin, self).get_context_data(**kwargs)
        # try:
        #     热门文章
        #     context['hot_article_list'] = \
        #         Article.objects.order_by("-view_times")[0:10]
        #     # 导航条
        #     context['nav_list'] = Nav.objects.filter(status=0)
        #     # 最新评论
        #     context['latest_comment_list'] = \
        #         Comment.objects.order_by("-create_time")[0:10]
        # except Exception as e:
        #     logger.error(u'[BaseMixin]加载基本信息出错')

        return context


class MainView(BaseMixin, ListView):
    template_name = 'art/index.html'

    def get_context_data(self, **kwargs):
        return super(MainView, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        # print "caole"
        # _img = r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\7.jpg"
        # # _img = "http://127.0.0.1:8000/static/img/6.jpg"
        # _str2img = Str2Img()
        # _path = _str2img.process(_img)
        #
        # mydict = {'url':_path}
        # return HttpResponse(
        #     json.dumps(mydict),
        #     content_type="application/json"
        # )


        data = request.POST['tx']
        # _width =  request.POST.get['width']

        # _height =  request.POST['height']
        # _charSize =  request.POST['char_size']

        print data , 'OK1'
        if not data:
            logger.error(
                u'[UserControl]用户上传头像为空:[%s]'.format(
                    request.user.username
                )
            )
            return HttpResponse(u"上传图片并选取区域", status=500)

        _width = int(self.request.POST.get("width", ""))
        _height = int(self.request.POST.get("height", ""))
        _charSize = int(self.request.POST.get("char_size", ""))
        _charAscii = self.request.POST.get("char_ascii", "")

        imgData = base64.b64decode(data)

        filename = "tx_100x100_{}.jpg".format(request.user.id)
        filedir = "art/static/img/"
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        path = filedir + filename

        file = open(path, "wb+")
        file.write(imgData)
        file.flush()
        file.close()

        # 修改头像分辨率
        im = Image.open(path)

        out = im.resize((100, 100), Image.ANTIALIAS)
        out.save(path)


        #Img To StrImg
        #return url
        _str2img = Str2Img()
        _url = _str2img.process(path,_width,_height,_charSize,_charAscii)
        mydict = {'url':_url}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )