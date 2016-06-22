# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gd_dispatch', '0005_auto_20160621_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='unix_timestamp',
            field=models.DateField(null=True, verbose_name='\u65f6\u95f4\u6233'),
        ),
        migrations.AddField(
            model_name='camera',
            name='uuid',
            field=models.CharField(max_length=128, null=True, verbose_name='\u5e8f\u5217\u53f7'),
        ),
    ]
