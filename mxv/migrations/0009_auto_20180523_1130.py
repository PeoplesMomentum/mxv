# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-23 10:30
from __future__ import unicode_literals

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mxv', '0008_auto_20180523_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconsent',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(help_text='Enter your email address to receive emails from Momentum', max_length=255, unique=True),
        ),
    ]