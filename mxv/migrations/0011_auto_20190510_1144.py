# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-10 10:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mxv', '0010_auto_20180523_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsettings',
            name='activation_email',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='mxv.Email'),
        ),
    ]
