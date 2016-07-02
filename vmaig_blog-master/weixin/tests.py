# -*- coding: utf-8 -*-
import httplib, urllib,urllib2
import json
if __name__ == '__main__':

    #http://127.0.0.1:8000/art/wx_img_str
    httpClient = None
    try:

        # params = urllib.urlencode( {  "img_url":"http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"} )
        #
        # headers = {"Content-type":"application/json"}
        # # headers = {"Content-type": "application/x-www-form-urlencoded" , "Accept": "json/plain"}
        # # "application/json"
        #
        # httpClient = httplib.HTTPConnection("127.0.0.1", 8000, timeout=30)
        #
        # httpClient.request("POST", "/art/wx_img_str", params, headers)
        #
        # response = httpClient.getresponse()
        # # print response.status
        # # print response.reason
        # print response.read()
        #
        # obj = json.loads('{"url": "/static/img/art/str_20160702155007.jpg"}')
        # print "1:",obj
        #
        # res = response.read()
        #
        # mydict = {"url":"11.txt"}
        #
        # dict = json.dumps(mydict)
        #
        # obj = json.loads(res)
        #
        #
        # print "2:",obj['url']
        # print response.getheaders() #获取头信息

        url = "http://127.0.0.1:8000/art/wx_img_str"
        data  = {  "img_url":"http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"}
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        res = response.read()
        # print response.read()
        obj = json.loads(res)
        print obj['url']
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()