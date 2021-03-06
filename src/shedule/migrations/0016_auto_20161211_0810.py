# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 08:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shedule', '0015_auto_20161130_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='pub_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время публикации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='upd_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Последнее изменение'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='weekday',
            field=models.IntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], default=6, verbose_name='День недели'),
        ),
    ]
