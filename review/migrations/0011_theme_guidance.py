# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-22 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_remove_track_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='guidance',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
