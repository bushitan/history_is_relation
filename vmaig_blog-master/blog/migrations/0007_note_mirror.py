# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160510_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='mirror',
            field=models.TextField(null=True, verbose_name='\u9274', blank=True),
        ),
    ]
