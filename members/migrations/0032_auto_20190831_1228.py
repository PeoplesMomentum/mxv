# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-31 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0031_auto_20190831_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
                ('display_order', models.IntegerField(default=members.models.next_campaign_tag_display_order)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignTagGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.TextField()),
                ('footer', models.TextField()),
                ('display_order', models.IntegerField(default=members.models.next_campaign_tag_group_display_order)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_groups', to='members.UpdateDetailsCampaign')),
            ],
        ),
        migrations.AddField(
            model_name='campaigntag',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='members.CampaignTagGroup'),
        ),
    ]
