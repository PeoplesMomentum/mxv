# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-29 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0020_auto_20180125_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='summary',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='proposalhistory',
            name='summary',
            field=models.CharField(default='', max_length=500),
        ),
    ]
