# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-22 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0081_auto_20170722_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='days',
            field=models.IntegerField(default=-1, verbose_name='\u0421\u0440\u043e\u043a (\u0434\u043d\u0435\u0439)'),
        ),
    ]