# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150514_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u540d\u79f0')),
                ('occur_date', models.DateTimeField(verbose_name='\u53d1\u751f\u65f6\u95f4')),
                ('mirror', models.TextField(null=True, verbose_name='\u9274', blank=True)),
            ],
            options={
                'verbose_name': '\u5386\u53f2\u6545\u4e8b',
                'verbose_name_plural': '\u5386\u53f2\u6545\u4e8b',
            },
        ),
    ]
