# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-09-03 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0039_campaignfield_is_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilefield',
            name='is_phone_number',
            field=models.BooleanField(default=False),
        ),
    ]