# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20180104_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_ncg_officer',
        ),
        migrations.AddField(
            model_name='member',
            name='is_members_council',
            field=models.BooleanField(default=False, verbose_name="Members' council (can act on behalf of the member's council)"),
        ),
    ]
