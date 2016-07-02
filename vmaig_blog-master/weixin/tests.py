# -*- coding: utf-8 -*-
import httplib, urllib

if __name__ == '__main__':

    #http://127.0.0.1:8000/art/wx_img_str
    httpClient = None
    try:

        params = urllib.urlencode( {  "img_url":"http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"} )

        headers = {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"}

        httpClient = httplib.HTTPConnection("127.0.0.1", 8000, timeout=30)

        httpClient.request("POST", "/art/wx_img_str", params, headers)
        print '2'
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