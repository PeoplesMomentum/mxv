# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 09:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amendment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(max_length=4000)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amendments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AmendmentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('text', models.TextField(max_length=4000)),
                ('amendment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='review.Amendment')),
            ],
        ),
        migrations.CreateModel(
            name='Nomination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominated_at', models.DateTimeField(auto_now_add=True)),
                ('nominated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=4000)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProposalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=4000)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='review.Proposal')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=1000)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('proposal_deadline', models.DateTimeField()),
                ('nomination_deadline', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='theme',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='review.Track'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='review.Theme'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominations', to='review.Proposal'),
        ),
        migrations.AddField(
            model_name='amendment',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amendments', to='review.Proposal'),
        ),
    ]
