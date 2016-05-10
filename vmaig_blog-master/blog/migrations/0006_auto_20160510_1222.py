# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160509_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='occur_date',
            field=models.DateField(null=True, verbose_name='\u53d1\u751f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='story',
            name='death_date',
            field=models.DateField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='story',
            name='occur_date',
            field=models.DateField(null=True, verbose_name='\u53d1\u751f\u65f6\u95f4'),
        ),
    ]
