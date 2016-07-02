# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree
from time import time
import httplib, urllib ,urllib2
import json
import hashlib

@csrf_exempt
def Index(request):
    if request.method=='GET':
        response=HttpResponse(CheckSignature(request))
        return response

    elif request.method=='POST':
        # service
        reply_msg = AutoReplyService(request)
        return reply_msg
    else:
        return HttpResponse('Hello World')

def CheckSignature(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)

    token='tan'

    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    if tmpstr==signature:
        return echostr
    else:
        return None

def AutoReplyService(request):

    # change to etree method
    message_str =  request.read()
    root = ElementTree.fromstring(message_str)
    form_user_name = root.find('FromUserName').text
    to_user_name = root.find('ToUserName').text
    message_type = root.find('MsgType').text

    context = {'to_user_name':form_user_name,'from_user_name':to_user_name}




    if message_type == 'image':
        image_url = root.find('PicUrl').text

        # text_xml = '''
        #     <xml>
        #     <ToUserName><![CDATA[%s]]></ToUserName>
        #     <FromUserName><![CDATA[%s]]></FromUserName>
        #     <CreateTime>%s</CreateTime>
        #     <MsgType><![CDATA[%s]]></MsgType>
        #     <Content><![CDATA[%s]]></Content>
        #     </xml>
        # '''

        text_img_xml = '''
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>

            <ArticleCount>1</ArticleCount>
            <Articles>
            <item>
            <Title><![CDATA[字符画]]></Title>
            <Description><![CDATA[description1]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>
            </Articles>
            </xml>
        '''


        message_type = 'news'

        # url process img to str

        def ImgToStr(url,data):

            req = urllib2.Request(url)
            data = urllib.urlencode(data)
            #enable cookie
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(req, data)
            res = response.read()
            # print response.read()
            obj = json.loads(res)
            return obj['url']


        url = "http://120.27.97.33/art/wx_img_str"
        data  = {  "img_url":image_url}
        _url = "http://120.27.97.33" + ImgToStr(url,data)

        content = "<a href='"+_url+"'>image url</a>"
        #answer content

        create_time = int(time())
        # c = {
        #     'to_user_name':context['to_user_name'],
        #     'from_user_name':context['from_user_name'],
        #     'create_time':create_time,
        #     'message_type':message_type,
        #     'content':content
        # }
        text_img = {
            'to_user_name':context['to_user_name'],
            'from_user_name':context['from_user_name'],
            'create_time':create_time,
            'message_type':message_type,
            'pic_url':_url,
            'url':_url
        }

        # text_reply_xml = text_xml % (c['to_user_name'],c['from_user_name'],c['create_time'],c['message_type'],c['content'])
        text_reply_xml = text_img_xml % (text_img['to_user_name'],text_img['from_user_name'],text_img['create_time'],text_img['message_type'],text_img['pic_url'],text_img['url'])


        response = HttpResponse(text_reply_xml,content_type='application/xml; charset=utf-8')

        return response
