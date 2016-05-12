# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vmaig_comments', '0002_auto_20160512_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='style',
        ),
    ]
