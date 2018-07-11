# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-10 16:58
from __future__ import unicode_literals

import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Intention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', django.contrib.postgres.fields.citext.CIEmailField(max_length=255, unique=True, verbose_name='email address')),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentions', to='voting_intentions.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='UrlParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('redirect_url', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='urlparameter',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='url_parameters', to='voting_intentions.Vote'),
        ),
        migrations.AddField(
            model_name='intention',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentions', to='voting_intentions.Vote'),
        ),
        migrations.AddField(
            model_name='choice',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='voting_intentions.Vote'),
        ),
    ]
