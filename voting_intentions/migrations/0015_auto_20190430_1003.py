# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-30 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_intentions', '0014_populate_choice_numbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='redirect_url',
            field=models.TextField(blank=True, default=''),
        ),
    ]