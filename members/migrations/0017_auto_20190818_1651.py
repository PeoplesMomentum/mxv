# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-18 15:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_auto_20190721_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='login_email_verification_key',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='new_login_email',
            field=django.contrib.postgres.fields.citext.CIEmailField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
