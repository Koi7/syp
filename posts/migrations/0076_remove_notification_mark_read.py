# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-11 23:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0075_auto_20170711_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='mark_read',
        ),
    ]
