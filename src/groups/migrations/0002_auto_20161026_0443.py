# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultygroup',
            name='id',
        ),
        migrations.AlterField(
            model_name='facultygroup',
            name='group_number',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]