# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-29 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_emailtarget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtarget',
            name='sent',
            field=models.NullBooleanField(default=None),
        ),
    ]
