# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-29 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0006_consultation_display_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='redirect_url',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]