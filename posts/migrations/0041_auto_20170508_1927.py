# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-08 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0040_vkusernotification'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VKUserNotification',
            new_name='Notification',
        ),
    ]
