# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 16:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shedule', '0012_auto_20161112_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shedule',
            name='group',
        ),
        migrations.DeleteModel(
            name='Shedule',
        ),
    ]