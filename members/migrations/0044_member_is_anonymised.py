# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-03-02 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0043_auto_20191028_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_anonymised',
            field=models.BooleanField(default=False, verbose_name='Personal data has been anonymised'),
        ),
    ]