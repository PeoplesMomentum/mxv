# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-22 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0012_auto_20190815_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultUrlParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the URL parameter to pass on when redirecting', max_length=100)),
                ('pass_on_name', models.CharField(blank=True, default=None, help_text='Set this to pass the parameter on with a different name', max_length=100, null=True)),
                ('nation_builder_value', models.CharField(blank=True, default=None, help_text='The value for this parameter in the NationBuilder URL above', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the URL parameter to pass on when redirecting', max_length=100)),
                ('pass_on_name', models.CharField(blank=True, default=None, help_text='Set this to pass the parameter on with a different name', max_length=100, null=True)),
                ('nation_builder_value', models.CharField(blank=True, default=None, help_text='The value for this parameter in the NationBuilder URL above', max_length=100, null=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='url_parameters', to='consultations.Consultation')),
            ],
        ),
    ]
