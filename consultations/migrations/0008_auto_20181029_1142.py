# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-29 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0007_auto_20181029_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='multipleAnswersAllowed',
            field=models.BooleanField(verbose_name='Multiple answers allowed'),
        ),
    ]
