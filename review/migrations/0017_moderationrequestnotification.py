# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-25 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0016_auto_20180124_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationRequestNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(default='', max_length=254)),
            ],
        ),
    ]