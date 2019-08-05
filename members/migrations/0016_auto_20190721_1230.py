# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-21 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import members.models


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
                ('field_type', models.CharField(choices=[('Char', 'Single line text'), ('Integer', 'Integer'), ('Decimal', 'Decimal'), ('Boolean', 'Checkbox (true/false)'), ('Email', 'Email')], default=members.models.MemberEditableFieldType('Single line text'), max_length=8)),
                ('required', models.BooleanField(default=False)),
                ('display_text', models.CharField(default='', max_length=255)),
                ('display_order', models.IntegerField(default=1)),
                ('admin_only', models.BooleanField(default=True)),
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
        migrations.AddField(
            model_name='member',
            name='nation_builder_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='MomentumGroup',
        ),
    ]