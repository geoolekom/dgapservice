# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 03:50
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shedule', '0004_remove_shedule_day_of_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='shedule',
            name='day_of_week',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='shedule',
            name='lesson_number',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)]),
        ),
    ]