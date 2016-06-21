# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gd_dispatch', '0003_auto_20160621_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelMonitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('camera', models.ForeignKey(verbose_name='\u6444\u50cf\u5934', to='gd_dispatch.Camera')),
                ('stb', models.ForeignKey(verbose_name='\u673a\u9876\u76d2', to='gd_dispatch.STB')),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u7ed1\u5b9a',
                'verbose_name_plural': '\u76d1\u63a7\u7ed1\u5b9a',
            },
        ),
    ]
