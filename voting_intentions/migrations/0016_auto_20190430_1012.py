# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-30 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_intentions', '0015_auto_20190430_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='redirect_url',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='choicetag',
            name='text',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='urlparameter',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='urlparameter',
            name='pass_on_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='votetag',
            name='text',
            field=models.CharField(max_length=100),
        ),
    ]