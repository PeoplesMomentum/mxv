# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-25 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_intentions', '0008_intention_tags_written_to_nation_builder'),
    ]

    operations = [
        migrations.AddField(
            model_name='intention',
            name='email_unknown_in_nation_builder',
            field=models.BooleanField(default=False),
        ),
    ]
