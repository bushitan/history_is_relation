# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from vmaig_comments.models import Comment
from blog.models import Note
import json

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from django.shortcuts import render,render_to_response
NoteModel = Note
# logger
logger = logging.getLogger(__name__)


# Create your views here.

class CommentControl(View):


    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 获取评论
        comment = self.request.POST.get("comment", "")


        _story_id = self.kwargs.get('story_id', '')
        _note_id = self.kwargs.get('note_id', '')

        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            logger.error(
                u'[CommentControl]当前用户非活动用户:[{}]'.format(
                    user.username
                )
            )
            return HttpResponse(u"请登陆！", status=403)
        if not comment:
            logger.error(
                u'[CommentControl]当前用户输入空评论:[{}]'.format(
                    user.username
                )
            )
            return HttpResponse(u"请输入评论内容！", status=403)

        # en_title = self.kwargs.get('slug', '')
        try:
            # 默认使用pk来索引(也可根据需要使用title,en_title在索引
            _note = NoteModel.objects.get(id=_note_id)
        except NoteModel.DoesNotExist:
            logger.error(u'[CommentControl]此便签不存在:[%s]' % _note_id)
            raise PermissionDenied

        # 保存评论
        comment = Comment.objects.create(
                user=user,
                note=_note,
                comment=comment,
                )

        try:
            img = comment.user.img
        except Exception as e:
            img = "http://vmaig.qiniudn.com/image/tx/tx-default.jpg"

        # 返回当前评论
        # html = "<li>\
        #             <div class=\"vmaig-comment-tx\">\
        #                 <img src={} width=\"40\"></img>\
        #             </div>\
        #             <div class=\"vmaig-comment-content\">\
        #                 <a><h1>{}</h1></a>\
        #                 <p>评论：{}</p>\
        #                 <p>{}</p>\
        #             </div>\
        #         </li>".format(
        #             img,
        #             comment.user.username,
        #             comment.comment,
        #             comment.create_time.strftime("%Y-%m-%d %H:%I:%S")
        #         )
        #
        # return HttpResponse(html)

        mydict = {
            "img": img,
            'username':comment.user.username,
            "comment": comment.comment,
            "time": comment.create_time.strftime("%Y-%m-%d %H:%I:%S")
        }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

class UploadView(View):
    template_name = 'vmaig_comments/upload.html'

    def get(self, request, *args, **kwargs):
        # print "OK"
        # return "a"
        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'bK5xWj0a-TBIljlxHYOHuQib9HYF_9Ft-HtP8tEb'
        secret_key = '56lucORYc45sF5eDqNk63mLXsQ78n4RrubIrjtE0'

        #构建鉴权对象
        q = Auth(access_key, secret_key)

        #要上传的空间
        bucket_name = 'clickz'

        #上传到七牛后保存的文件名
        key = 'my-python-logo.png';

        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)

        return render_to_response('vmaig_comments/upload.html',{'token':token})
         # token