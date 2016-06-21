from gd_dispatch.models import *


_stbsn="44290068159"
_stb = STB.objects.get(sn=_stbsn)#获取stb
print "stb",_stb
_m = RelMonitor.objects.filter(stb=_stb)#获取监控关系列表