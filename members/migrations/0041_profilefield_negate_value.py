# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-09-03 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0040_profilefield_is_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilefield',
            name='negate_value',
            field=models.BooleanField(default=False, help_text='Use with Checkbox fields only, returns True instead of False and vice versa'),
        ),
    ]
