# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings



class string_with_title(str):
    """ 用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,
    所以修改str类的title方法就可以实现.
    """
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class STB(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'户主名称')
    sn = models.CharField(max_length=40, verbose_name=u'序列号')

    class Meta:
        verbose_name_plural = verbose_name = u"信息_机顶盒"
        # app_label = string_with_title('gd_dispatch', u"广电调度平台")
        app_label = string_with_title('gd_dispatch', u"广电调度平台")
    def __unicode__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'户主名称')
    sn = models.CharField(max_length=40, verbose_name=u'序列号')
    ip = models.GenericIPAddressField(verbose_name=u'IP地址')
    class Meta:
        verbose_name_plural = verbose_name = u"信息_摄像头"
        # app_label = string_with_title('gd_dispatch', u"广电调度平台")
        app_label = string_with_title('gd_dispatch', u"广电调度平台")
    def __unicode__(self):
        return self.name


class RelMonitor(models.Model):
    stb = models.ForeignKey(STB, verbose_name=u'机顶盒')
    camera = models.ForeignKey(Camera, verbose_name=u'摄像头')
    class Meta:
        verbose_name_plural = verbose_name = u'绑定_监控'
        app_label = string_with_title(u'gd_dispatch', u"监控")


class RelPhone(models.Model):
    stb = models.ForeignKey(STB, verbose_name=u'机顶盒')
    camera = models.ForeignKey(Camera, verbose_name=u'摄像头')
    class Meta:
        verbose_name_plural = verbose_name = u'绑定_可视电话'
        app_label = string_with_title(u'gd_dispatch', u"可视电话")

