# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-16 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190415_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='finish',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='result',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]