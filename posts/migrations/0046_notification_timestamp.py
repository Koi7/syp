# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-13 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0045_auto_20170513_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
