# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-13 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0044_auto_20170513_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='actor_object_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
