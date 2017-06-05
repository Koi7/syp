# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-13 16:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('posts', '0043_auto_20170508_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='actor_content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_actor', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='notification',
            name='actor_object_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='verb',
            field=models.CharField(choices=[(-1, 'no'), (0, 'like'), (1, 'message'), (2, 'published'), (3, 'unpublished')], default=-1, max_length=20),
        ),
    ]