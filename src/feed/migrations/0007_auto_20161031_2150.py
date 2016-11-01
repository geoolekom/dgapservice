# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='entry',
            field=models.TextField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upd_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Последнее изменение'),
        ),
        migrations.AlterField(
            model_name='post',
            name='entry',
            field=models.TextField(verbose_name='Текст поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='upd_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Последнее изменение'),
        ),
    ]
