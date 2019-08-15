# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-15 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0011_auto_20190415_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='post_questions_text',
            field=models.TextField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='pre_questions_text',
            field=models.TextField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='guidance',
            field=models.TextField(blank=True, default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(max_length=2000),
        ),
    ]
