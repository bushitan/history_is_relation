# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160507_0009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'verbose_name': '\u5386\u53f2\u4fbf\u7b7e', 'verbose_name_plural': '\u5386\u53f2\u4fbf\u7b7e'},
        ),
        migrations.AlterModelOptions(
            name='relstorynote',
            options={'verbose_name': '\u5386\u53f2\u6545\u4e8b\u4fbf\u7b7e\u5173\u7cfb', 'verbose_name_plural': '\u5386\u53f2\u6545\u4e8b\u4fbf\u7b7e\u5173\u7cfb'},
        ),
    ]
