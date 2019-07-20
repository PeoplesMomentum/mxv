# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-20 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20190510_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberEditableNationBuilderField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_path', models.CharField(max_length=255)),
                ('field_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='momentumgroup',
            name='primary_contact',
        ),
        migrations.RemoveField(
            model_name='member',
            name='momentum_group',
        ),
        migrations.DeleteModel(
            name='MomentumGroup',
        ),
    ]
