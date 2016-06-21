from django.contrib import admin
from gd_dispatch.models import *
# Register your models here.


class STBAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(STB,STBAdmin)


class CameraAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Camera,CameraAdmin)


class RelMonitorAdmin(admin.ModelAdmin):
    list_display = ('stb','camera')
admin.site.register(RelMonitor,RelMonitorAdmin)

class RelPhoneAdmin(admin.ModelAdmin):
    list_display = ('stb','camera')
admin.site.register(RelPhone,RelPhoneAdmin)