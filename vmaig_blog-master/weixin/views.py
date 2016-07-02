# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree
from time import time
import httplib, urllib
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

        text_xml = '''
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>
        '''

        message_type = 'text'

        # url process img to str
        httpClient = None
        response = None
        try:

            params = urllib.urlencode( {  "img_url":"http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"} )

            headers = {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"}

            httpClient = httplib.HTTPConnection("127.0.0.1", 8000, timeout=30)

            httpClient.request("POST", "/art/wx_img_str", params, headers)

            response = httpClient.getresponse()
            print response.status
            print response.reason
            print response.read()
            print response.getheaders() #获取头信息
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()

        if response:
            response.read()["url"]

        #answer content
        content = "<a href='"+image_url+"'>image url</a>"
        create_time = int(time())
        c = {
            'to_user_name':context['to_user_name'],
            'from_user_name':context['from_user_name'],
            'create_time':create_time,
            'message_type':message_type,
            'content':content
        }

        text_reply_xml = text_xml % (c['to_user_name'],c['from_user_name'],c['create_time'],c['message_type'],c['content'])

        response = HttpResponse(text_reply_xml,content_type='application/xml; charset=utf-8')

        return response
