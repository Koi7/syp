# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-22 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0080_auto_20170719_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='brand_ofsite',
            field=models.CharField(default='', max_length=150, verbose_name='\u0421\u0430\u0439\u0442 \u0431\u0440\u044d\u043d\u0434\u0430'),
        ),
        migrations.AddField(
            model_name='ad',
            name='days',
            field=models.IntegerField(choices=[(-1, '\u0412\u0441\u0435'), (0, '\u0421\u0435\u0432\u0430\u0441\u0442\u043e\u043f\u043e\u043b\u044c'), (1, '\u0421\u0438\u043c\u0444\u0435\u0440\u043e\u043f\u043e\u043b\u044c'), (2, '\u042f\u043b\u0442\u0430')], default=-1, verbose_name='\u0421\u0440\u043e\u043a (\u0434\u043d\u0435\u0439)'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='brand_icon',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.get_ad_image_path, verbose_name='\u041b\u043e\u0433\u043e\u0442\u0438\u043f'),
        ),
    ]