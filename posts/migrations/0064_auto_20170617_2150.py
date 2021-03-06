# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-17 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0063_auto_20170611_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vk_id', models.CharField(default='', max_length=20, verbose_name='VK_ID')),
                ('reason', models.CharField(default='', max_length=250, verbose_name='\u041f\u0440\u0438\u0447\u0438\u043d\u0430')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('days', models.IntegerField(default=-1)),
            ],
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='age',
            field=models.IntegerField(default=0, verbose_name='\u0412\u043e\u0437\u0440\u0430\u0441\u0442'),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='place',
            field=models.IntegerField(choices=[(0, '\u0421\u0435\u0432\u0430\u0441\u0442\u043e\u043f\u043e\u043b\u044c'), (1, '\u0421\u0438\u043c\u0444\u0435\u0440\u043e\u043f\u043e\u043b\u044c'), (2, '\u042f\u043b\u0442\u0430')], default=1, verbose_name='\u0413\u043e\u0440\u043e\u0434'),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='sex',
            field=models.IntegerField(choices=[(-1, '\u043d\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043e'), (0, '\u043f\u0430\u0440\u0435\u043d\u044c'), (1, '\u0434\u0435\u0432\u0443\u0448\u043a\u0430')], default=-1, verbose_name='\u041f\u043e\u043b'),
        ),
    ]
