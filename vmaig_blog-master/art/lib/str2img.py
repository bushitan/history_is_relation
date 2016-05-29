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
    def get_char(self,r,b,g,alpha = 256):
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
        filedir = "art/static/img/"
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        url = filedir + filename
        # strImg.save(r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\img2.png")
        # strImg.save(r"art/static/img/img3.png")
        print url
        strImg.save(url)
        return r"/static/img/"+filename

# if __name__ == '__main__':
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