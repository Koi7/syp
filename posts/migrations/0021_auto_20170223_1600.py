# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-23 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_auto_20170223_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuser',
            name='place',
            field=models.IntegerField(choices=[(0, '\u0421\u0435\u0432\u0430\u0441\u0442\u043e\u043f\u043e\u043b\u044c'), (1, '\u0421\u0438\u043c\u0444\u0435\u0440\u043e\u043f\u043e\u043b\u044c'), (2, '\u042f\u043b\u0442\u0430')], default=1),
        ),
    ]
