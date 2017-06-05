# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-23 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0056_auto_20170523_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='verb',
            field=models.CharField(choices=[(-1, 'no'), (0, '\u043b\u0430\u0439\u043a\u043d\u0443{} \u0432\u0430\u0448 \u0430\u043a\u0443\u0442\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0441\u0442.'), (1, '\u043e\u0441\u0442\u0430\u0432\u0438{} \u043f\u043e\u0441\u043b\u0430\u043d\u0438\u0435 \u043a \u0432\u0430\u0448\u0435\u043c\u0443 \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u043c\u0443 \u043f\u043e\u0441\u0442\u0443.'), (2, '\u0412\u0430\u0448 \u043f\u043e\u0441\u0442 \u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d.'), (3, '\u0412\u0430\u0448 \u043f\u043e\u0441\u0442 \u043d\u0430\u0440\u0443\u0448\u0430\u0435\u0442 \u043f\u0440\u0430\u0432\u0438\u043b\u0430 \u0441\u0430\u0439\u0442\u0430, \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u043e\u043d \u043d\u0435 \u0431\u0443\u0434\u0435\u0442 \u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d.')], default=-1, max_length=100),
        ),
    ]