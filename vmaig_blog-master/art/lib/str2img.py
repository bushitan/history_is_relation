#--coding:utf-8--
from PIL import Image,ImageDraw,ImageFont
# import argparse
#
# #命令行输入参数处理
# parser = argparse.ArgumentParser()
#
# parser.add_argument('file')     #输入文件
# parser.add_argument('-o', '--output')   #输出文件
# parser.add_argument('--width', type = int, default = 80) #输出字符画宽
# parser.add_argument('--height', type = int, default = 80) #输出字符画高

#获取参数
# args = parser.parse_args()
#
# IMG = args.file
# WIDTH = args.width
# HEIGHT = args.height
# OUTPUT = args.output
# IMG = r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\6.jpg"
# WIDTH = 160
# HEIGHT = 90
# # OUTPUT = '2.txt'
# _charSize = 8

#
# ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
# ascii_char = list(u"0-. ")
import  os
import  time
class Str2Img():
    ascii_char = list(u"0-. ")
    # 将256灰度映射到70个字符上
    def get_char(self,r,g,b,alpha = 256):
        if alpha == 0:
            return ' '
        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        unit = (256.0 + 1)/length
        return self.ascii_char[int(gray/unit)]

    def process(self,IMG,WIDTH=160,HEIGHT=90,_charSize=5,_charAscii="0-. "):

        self.ascii_char = list(_charAscii)
        im = Image.open(IMG)
        im = im.resize((WIDTH,HEIGHT), Image.NEAREST)


        strImg = Image.new("RGBA",(WIDTH*_charSize,HEIGHT*_charSize),(255,255,255))
        font = ImageFont.truetype ('simsun.ttc', _charSize)
        a=ImageDraw.Draw(strImg)

        for i in range(HEIGHT):
            for j in range(WIDTH):
                _char = self.get_char(*im.getpixel((j,i)))
                a.text((j*_charSize,i*_charSize),_char,fill=(0,0,0),font=font)

        filename = "tx_100x100_{}.jpg".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        # filedir = r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img"
        filedir = "art/static/img/"
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        url = filedir + filename
        # strImg.save(r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\img2.png")
        # strImg.save(r"art/static/img/img3.png")
        print url
        strImg.save(url)
        return r"/static/img/"+filename


    def RGB_Average(self,r,g,b,alpha=256):
        if alpha == 0:
            return ' '

        #把每个单色模块中255色压缩为16色
        def average(n):
            return ( n /16 + 1 ) * 16 - 8
            # return ( n /32 + 1 ) * 32 - 16
        _r = average(r)
        _g = average(g)
        _b = average(b)

        return ( _r,_g,_b )

    def test_Pixel_Img(self,IMG,WIDTH=100,HEIGHT=80,_charSize=5):
        im = Image.open(IMG)
        im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

        strImg = Image.new("RGBA",(WIDTH*_charSize,HEIGHT*_charSize),(255,255,255))
        _draw  =ImageDraw.Draw(strImg)

        # r,g,b = im.getpixel((10,10))
        # print  r,g,b
        # R,G,B = self.RGB_Average( r,g,b)
        # print R,G,B
        # im.putpixel((j,i), (R,G,B))

        for i in range(HEIGHT):
            for j in range(WIDTH):
                 # R,G,B = self.RGB_Average(*im.getpixel((j,i)))
                 r,g,b = im.getpixel((j,i))
                 R,G,B = self.RGB_Average( r,g,b)
                 # im.putpixel((j,i), (R,G,B))
                 _draw.rectangle ( (j*5,i*5,j*5+5,i*5+5) , fill=(R,G,B) )
                 # _draw.rectangle ( (j*5,i*5,j*5+5,i*5+5) , fill=(G,B,R) )
                 # _draw.rectangle ( (j*5,i*5,j*5+5,i*5+5) , fill=(B,R,G) )
                 # _draw.rectangle ( (j*5,i*5,j*5+5,i*5+5) , fill=(G,R,B) )
        #         _char = self.RGB_Average(*im.getpixel((j,i)))
        #         _draw.rectangle ( (10,10,50,50) , fill=255 )
                # a.text((j*_charSize,i*_charSize),_char,fill=(0,0,0),font=font)

        # _pixel = self.RGB_Average(*im.getpixel((5,5)))
        # R,G,B = self.RGB_Average(*im.getpixel((50,25)))
        # _draw.rectangle ( (10,10,5,5) , fill=(_pixel.R,_pixel.G,_pixel.B) )
        # _draw.rectangle ( (5,5,0,0) , fill=(R,G,B) )
        # _draw.rectangle ( (5,5,0,0) , fill=(B,G,R) )
        # _draw.rectangle ( (5,5,0,0) , fill=(R,G,B) )

        filename = "\pixel_100x100_{}.png".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        filedir = r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img"
        url = filedir + filename
        strImg.save(url,"png")

        # filename = "\pixel_100x100_{}.png".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        # filedir = r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img"
        # url = filedir + filename
        # im.save(url,"png")

if __name__ == '__main__':
    _s = Str2Img()
    _s.test_Pixel_Img(r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img\7.jpg" , 50,40)
    # _s.process(r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img\7.jpg",100,80)

    n = 16
    print ( n /16 + 1 ) * 16 -8
#
#     im = Image.open(IMG)
#     im = im.resize((WIDTH,HEIGHT), Image.NEAREST)
#
#     txt = ""
#
#     # for i in range(HEIGHT):
#     #     for j in range(WIDTH):
#     #         txt += get_char(*im.getpixel((j,i)))
#     #     txt += '\n'
#     #
#     # print txt
#
#
#     strImg = Image.new("RGBA",(WIDTH*_charSize,HEIGHT*_charSize),(255,255,255))
#     font = ImageFont.truetype ('simsun.ttc', _charSize)
#     a=ImageDraw.Draw(strImg)
#
#     for i in range(HEIGHT):
#         for j in range(WIDTH):
#             _char = get_char(*im.getpixel((j,i)))
#
#             a.text((j*_charSize,i*_charSize),_char,fill=(0,0,0),font=font)
#             # txt += get_char(*im.getpixel((j,i)))
#
#     strImg.save("img2.png")


    #字符画输出到文件
    # if OUTPUT:
    #     with open(OUTPUT,'w') as f:
    #         f.write(txt)
    # else:
    #     with open("output.txt",'w') as f:
    #         f.write(txt)