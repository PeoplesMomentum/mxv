# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-26 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0024_auto_20180226_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackvoting',
            name='track',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voting', to='review.Track'),
        ),
    ]
