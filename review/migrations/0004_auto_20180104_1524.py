# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-04 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20180104_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='nomination_deadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='track',
            name='start',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='track',
            name='submission_deadline',
            field=models.DateField(),
        ),
    ]
