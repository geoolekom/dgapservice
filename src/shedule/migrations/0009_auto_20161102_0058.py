# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shedule', '0008_auto_20161101_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shedule',
            name='room',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Аудитория'),
        ),
    ]
