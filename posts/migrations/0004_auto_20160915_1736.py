# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 14:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160910_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vk_user',
            old_name='have_active_post',
            new_name='has_active_post',
        ),
        migrations.RenameField(
            model_name='vk_user',
            old_name='photo_rec_url',
            new_name='photo_rec',
        ),
    ]
