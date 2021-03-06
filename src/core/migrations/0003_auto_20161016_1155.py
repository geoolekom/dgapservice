# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161016_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='media/avatars', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='group_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='Group'),
        ),
    ]
