# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-30 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_intentions', '0018_auto_20190430_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlparameter',
            name='nation_builder_value',
            field=models.CharField(blank=True, default=None, help_text='The value for this parameter in the NationBuilder URL above', max_length=100, null=True),
        ),
    ]
