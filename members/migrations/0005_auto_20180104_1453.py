# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-04 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20171215_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='momentum_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='members.MomentumGroup'),
        ),
    ]
