# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-15 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurred_at', models.DateTimeField(auto_now_add=True)),
                ('error', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('finish', models.DateTimeField()),
                ('result', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateTimeField(blank=True, default=None, null=True)),
                ('repeat_seconds', models.IntegerField(blank=True, default=None, null=True)),
                ('repeat_count', models.IntegerField(blank=True, default=None, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('job_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SendEmailTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tasks.Task')),
            ],
            bases=('tasks.task',),
        ),
        migrations.CreateModel(
            name='VotingIntentionTagTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tasks.Task')),
            ],
            bases=('tasks.task',),
        ),
        migrations.AddField(
            model_name='task',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_tasks.task_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='run',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='error',
            name='run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='tasks.Run'),
        ),
    ]
