# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 12:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL),
        ),
    ]