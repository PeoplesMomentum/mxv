# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-28 10:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0026_PopulateNationBuilderPerson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='nation_builder_id',
        ),
    ]