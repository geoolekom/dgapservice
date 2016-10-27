# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 03:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_ratedpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='upd_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Last update'),
        ),
    ]
