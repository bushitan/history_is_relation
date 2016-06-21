# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gd_dispatch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='\u6237\u4e3b\u540d\u79f0')),
                ('sn', models.CharField(max_length=40, verbose_name='\u5e8f\u5217\u53f7')),
                ('ip', models.IPAddressField()),
            ],
            options={
                'verbose_name': '\u6444\u50cf\u5934\u4fe1\u606f',
                'verbose_name_plural': '\u6444\u50cf\u5934\u4fe1\u606f',
            },
        ),
    ]
