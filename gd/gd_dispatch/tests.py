from gd_dispatch.models import *


_stbsn="44290068159"
_stb = STB.objects.get(sn=_stbsn)#��ȡstb
print "stb",_stb
_m = RelMonitor.objects.filter(stb=_stb)#��ȡ��ع�ϵ�б�