# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-12 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0076_remove_notification_mark_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkuser',
            name='photo_large',
            field=models.CharField(default='', max_length=200),
        ),
    ]
