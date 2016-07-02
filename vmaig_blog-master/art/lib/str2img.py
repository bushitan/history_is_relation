#--coding:utf-8--
from PIL import Image,ImageDraw,ImageFont
import sys
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

    def process(self,IMG,WIDTH=160,HEIGHT=90,_charSize=10,_charAscii="0-. ",grid_num = 5):

        self.ascii_char = list(_charAscii)

        # 修改头像分辨率
        im = Image.open(IMG)
        im = im.resize((WIDTH,HEIGHT), Image.NEAREST)


        strImg = Image.new("RGBA",(WIDTH*_charSize,HEIGHT*_charSize),(255,255,255))
        # font = ImageFont.truetype ('simsun.ttc', _charSize)
        a=ImageDraw.Draw(strImg)

        for i in range(HEIGHT):
            for j in range(WIDTH):
                _char = self.get_char(*im.getpixel((j,i)))
                a.text((j*_charSize,i*_charSize),_char,fill=(0,0,0))


        #画方格
        _grid = grid_num
        if _grid != 0:
            _color = (130, 130, 130)
            for i in range(_grid):
                a.line([(0,i*HEIGHT*_charSize/_grid),(WIDTH*_charSize,i*HEIGHT*_charSize/_grid)],fill=_color,width=1)

            for i in range(_grid):
                a.line([(i*WIDTH*_charSize/_grid,0),(i*WIDTH*_charSize/_grid,HEIGHT*_charSize)],fill=_color,width=1)


        filename = "tx_100x100_{}.jpg".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        # filedir = r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img"
        # homedir = os.path.dirname(os.path.dirname(sys.path[0]))
        # print "homedir:",homedir
        # print "sys.path[0]:",sys.path[0]
        # parent_path = os.path.dirname(homedir)
        filedir = sys.path[0]+"/blog/static/img/art/"

        # print "homedir:" + homedir
        # print "filedir:" + filedir
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        url = filedir + filename
        # strImg.save(r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\img2.png")
        # strImg.save(r"art/static/img/img3.png")
        # print url
        strImg.save(url)
        # print "url:" + url
        return r"/static/img/art/"+filename

    #图片转化像素数组
    def ImgToMatrix(self,imgPath,WIDTH=50,HEIGHT=50):
        im = Image.open(imgPath)
        _matrix = []
        for i in range(HEIGHT):
            for j in range(WIDTH):
                r,g,b = im.getpixel((j,i)) #获取原始像素
                r,g,b = self.RGB_Average(r,g,b) #像素扁平化处理
                _matrix.append(self.rgb2hex(r,g,b))#rgb转16进制，入队
        return _matrix

    #css 专用的16进制表达方式
    def rgb2hex(self,r,g,b):
        _h = hex((r << 16) + (g << 8) + b)
        # _h = "#"+_h[2:].upper()
        _h =_h[2:] # 删除Ox
        _h = "#" + _h.zfill(6) #字符串用0补全6位

        return _h

    #16 进制转RGB
    def hex2rgb(self,hexcolor):
        hexcolor = int(hexcolor)
        rgb = [(hexcolor >> 16) & 0xff,
            (hexcolor >> 8) & 0xff,
            hexcolor & 0xff
        ]
        return rgb


    #像素扁平化
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

    def MatrixToImg(self,imgPath,matrix,WIDTH=50,HEIGHT=50,_pixelSize=5):

        _img = Image.new("RGBA",(WIDTH*_pixelSize,HEIGHT*_pixelSize),(255,255,255))
        _draw  =ImageDraw.Draw(_img)

        _matPos = 0
        for i in range(HEIGHT):
            for j in range(WIDTH):
                print i*WIDTH+j
                _hexStr = matrix[i*WIDTH+j]
                _hexStr = "0x" + _hexStr[1:]
                _hex = eval(_hexStr)
                R,G,B = self.hex2rgb(_hex)

                _draw.rectangle ( (j*_pixelSize,i*_pixelSize,j*_pixelSize+_pixelSize,i*_pixelSize+_pixelSize) , fill=(R,G,B) )

        _img.save(imgPath,"png")
        return True


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
                 print self.rgb2hex(r,g,b)
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
        # filedir = r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img"
        filedir = r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img"
        url = filedir + filename
        strImg.save(url,"png")

        # filename = "\pixel_100x100_{}.png".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        # filedir = r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img"
        # url = filedir + filename
        # im.save(url,"png")


    def Process_Adapt(self,width = 1080,height = 1970,_grid_numX = 4):

        _grid_offsetX = width % _grid_numX / 2
        _grid_length = (width - _grid_offsetX * 2) / _grid_numX

        _grid_numY = height / _grid_length  #Y的格子数


        _grid_offsetY = height % _grid_length / 2

        print height,_grid_numY,_grid_offsetY
        print height / _grid_numY
        # if height < _grid_length :
        #     return False

        _lines = []
        #横线
        for i in range(_grid_numY+1):
            _lines.append( (_grid_offsetX,_grid_offsetY + _grid_length*i,_grid_offsetX + _grid_length * _grid_numX , _grid_offsetY + _grid_length*i) )
        #竖线
        for i in range(_grid_numX+1):
            _lines.append( (_grid_offsetX + _grid_length * i,_grid_offsetY,_grid_offsetX + _grid_length * i , _grid_offsetY + _grid_length * _grid_numY) )
        # print _lines

        return _lines

    def Process_ByUrl(self,filedir , filename,_grid_numX = 4):

        im = Image.open(filedir+filename)
        # print "format:",im.format, "size:",im.size, "mode:",im.mode

        WIDTH = im.size[0]
        HEIGHT = im.size[1]
        _grid = _grid_numX
        _charSize = 1

        # out = im.resize((WIDTH,HEIGHT), Image.NEAREST)
        a = ImageDraw.Draw(im)

        _color = (130, 130, 130)

        if _grid > 0:
            # print _grid

            _lines = self.Process_Adapt(WIDTH,HEIGHT,_grid)

            for i in range(len(_lines)):
                # a.line(
                a.line([(_lines[i][0],_lines[i][1]),(_lines[i][2],_lines[i][3])],fill=_color,width=1)

        _strFilename = "str_{}.jpg".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        path = filedir + _strFilename
        im.save(path)
        return _strFilename

        # _url =   r"/static/img/art/"+filename

if __name__ == '__main__':
    _s = Str2Img()
    # _s.Process_Adapt()
    # _s.process("tx_100x100_None.jpg")
    # print _s.ImgToMatrix(r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\tx_100x100_1.jpg")
    # _s.test_Pixel_Img(r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img\compress_100x100_20160601233304.jpg" , 50,50)
    # _s.test_Pixel_Img(r"H:\Code\Python\Git\history_is_relation\vmaig_blog-master\art\static\img\compress_100x100_20160601233304.jpg" , 50,50)
    # _s.process(r"E:\Carcer World\code\Python\git\history_is_relation\vmaig_blog-master\art\static\img\7.jpg",100,80)
    # print _s.rgb2hex(157,24,68)
    # print _s.hex2rgb(0x9d1844)
    # homedir = os.getcwd()
    # parent_path = os.path.dirname(homedir)
    # print os.path.dirname(os.path.dirname(sys.path[0]))
    #
    # print homedir
    # print parent_path
    #
    # print _s.hex2rgb(0x9d181b)
    # print _s.hex2rgb(0x9d181b)
    #
    # a = '#c828282'
    # #
    # a = "0x" + a[1:]
    # b = eval(a)
    # print a,b
    # print _s.hex2rgb(b)


    # a = '0xe8e8e8'
    # b = eval(a)
    # print _s.hex2rgb(b)
    # b= hex(eval('0x154431'))


    # print _s.hex2rgb(b)
    #
    # print _s.rgb2hex(157,24,27)

    # def tt (r,g,b):
    #     print (r << 16) + (g << 8) + b
    #     print (r * 256* 256) + (g * 256) + b
    #
    # tt(8,131,24)


    # print hex("OxE8E8E8")

    # print 70/50
    # n = 16
    # print ( n /16 + 1 ) * 16 -8
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