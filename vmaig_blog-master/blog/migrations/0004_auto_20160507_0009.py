# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_story'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occur_date', models.DateTimeField(null=True, verbose_name='\u53d1\u751f\u65f6\u95f4')),
                ('mark', models.CharField(max_length=100, null=True, verbose_name='\u6807\u8bc6')),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0')),
                ('style', models.IntegerField(default=0, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab', choices=[(0, '\u5b9e'), (1, '\u9274')])),
            ],
            options={
                'verbose_name': '\u4fbf\u7b7e',
                'verbose_name_plural': '\u4fbf\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='RelStoryNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.ForeignKey(verbose_name='\u4fbf\u7b7e', to='blog.Note')),
            ],
            options={
                'verbose_name': '\u6545\u4e8b\u4fbf\u7b7e\u5173\u7cfb',
                'verbose_name_plural': '\u6545\u4e8b\u4fbf\u7b7e\u5173\u7cfb',
            },
        ),
        migrations.AddField(
            model_name='story',
            name='death_date',
            field=models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='story',
            name='occur_date',
            field=models.DateTimeField(null=True, verbose_name='\u53d1\u751f\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='relstorynote',
            name='story',
            field=models.ForeignKey(verbose_name='\u6545\u4e8b', to='blog.Story'),
        ),
    ]
