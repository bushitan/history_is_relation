#--coding:utf-8--
import os
import uuid
import urllib2
import cookielib


class Web():
    def Download_Img(self,filedir , filename, url):



        def get_file_extension(file):
            return os.path.splitext(file)[1]

        '''創建文件目录，并返回该目录'''
        def mkdir(path):
            # 去除左右两边的空格
            path=path.strip()
            # 去除尾部 \符号
            path=path.rstrip("\\")

            if not os.path.exists(path):
                os.makedirs(path)

            return path

        '''自动生成一个唯一的字符串，固定长度为36'''
        def unique_str():
            return str(uuid.uuid1())

        '''
        抓取网页文件内容，保存到内存

        @url 欲抓取文件 ，path+filename
        '''
        def get_file(url):
            try:
                cj=cookielib.LWPCookieJar()
                opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)

                req=urllib2.Request(url)
                operate=opener.open(req)
                data=operate.read()
                return data
            except BaseException, e:
                print e
                return None

        '''
        保存文件到本地

        @path  本地路径
        @file_name 文件名
        @data 文件内容
        '''
        def save_file(path, file_name, data):
            if data == None:
                return

            mkdir(path)
            if(not path.endswith("/")):
                path=path+"/"
            file=open(path+file_name, "wb")
            file.write(data)
            file.flush()
            file.close()


        # url="http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"


        try:
            # url = filedir + filename
            save_file(filedir, filename, get_file(url))
            path = filedir+filename
            return path
        except:
            return False


if __name__ == '__main__':
    w = Web()
    w.Download_Img()