# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-01 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20161228_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='place',
            field=models.CharField(default='', max_length=200),
        ),
    ]