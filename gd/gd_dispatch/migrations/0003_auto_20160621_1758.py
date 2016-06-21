# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gd_dispatch', '0002_camera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='ip',
            field=models.GenericIPAddressField(verbose_name='IP\u5730\u5740'),
        ),
    ]
