# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-22 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0032_auto_20170422_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuser',
            name='about',
            field=models.CharField(default=None, max_length=4000),
        ),
    ]
