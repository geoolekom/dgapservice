# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 03:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shedule', '0003_remove_shedule_youmom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shedule',
            name='day_of_week',
        ),
    ]
