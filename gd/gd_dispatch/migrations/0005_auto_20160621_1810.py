# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gd_dispatch', '0004_relmonitor'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelPhone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u7ed1\u5b9a_\u53ef\u89c6\u7535\u8bdd',
                'verbose_name_plural': '\u7ed1\u5b9a_\u53ef\u89c6\u7535\u8bdd',
            },
        ),
        migrations.AlterModelOptions(
            name='camera',
            options={'verbose_name': '\u4fe1\u606f_\u6444\u50cf\u5934', 'verbose_name_plural': '\u4fe1\u606f_\u6444\u50cf\u5934'},
        ),
        migrations.AlterModelOptions(
            name='relmonitor',
            options={'verbose_name': '\u7ed1\u5b9a_\u76d1\u63a7', 'verbose_name_plural': '\u7ed1\u5b9a_\u76d1\u63a7'},
        ),
        migrations.AlterModelOptions(
            name='stb',
            options={'verbose_name': '\u4fe1\u606f_\u673a\u9876\u76d2', 'verbose_name_plural': '\u4fe1\u606f_\u673a\u9876\u76d2'},
        ),
        migrations.AddField(
            model_name='relphone',
            name='camera',
            field=models.ForeignKey(verbose_name='\u6444\u50cf\u5934', to='gd_dispatch.Camera'),
        ),
        migrations.AddField(
            model_name='relphone',
            name='stb',
            field=models.ForeignKey(verbose_name='\u673a\u9876\u76d2', to='gd_dispatch.STB'),
        ),
    ]
