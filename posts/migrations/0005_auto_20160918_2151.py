# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 18:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20160915_1736'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VK_User',
            new_name='VKUser',
        ),
    ]
