# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-28 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0042_campaignfield_negate_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilefield',
            name='admin_only',
            field=models.BooleanField(default=False),
        ),
    ]
