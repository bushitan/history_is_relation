# -*- coding: utf-8 -*-
# flake8: noqa

from django.test import TestCase

# Create your tests here.
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
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
print token
#要上传文件的本地路径
# localfile = 't1.jpg'
#
# ret, info = put_file(token, key, localfile)
# print(info)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)