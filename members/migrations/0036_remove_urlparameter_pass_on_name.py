# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-09-02 08:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0035_auto_20190902_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlparameter',
            name='pass_on_name',
        ),
    ]
