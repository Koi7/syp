# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-18 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0064_auto_20170617_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimage',
            name='is_portrait',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blacklist',
            name='days',
            field=models.IntegerField(default=-1, verbose_name='\u0421\u0440\u043e\u043a'),
        ),
    ]
