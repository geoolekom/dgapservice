# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shedule', '0011_auto_20161102_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='weekday',
            field=models.IntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], default=5, verbose_name='День недели'),
        ),
    ]