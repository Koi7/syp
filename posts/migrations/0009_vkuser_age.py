# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-26 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20160921_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkuser',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
