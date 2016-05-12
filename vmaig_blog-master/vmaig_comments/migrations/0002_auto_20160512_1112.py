# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vmaig_comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='style',
            field=models.TextField(null=True, verbose_name='\u8bc4\u8bba\u98ce\u683c'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(null=True, verbose_name='\u8bc4\u8bba\u5185\u5bb9'),
        ),
    ]
