# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-16 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0021_auto_20180129_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='guidance',
        ),
    ]
