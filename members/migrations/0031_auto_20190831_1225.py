# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-31 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0030_campaignfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigntag',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='updatedetailscampaign',
            name='first_page_post_text',
        ),
        migrations.RemoveField(
            model_name='updatedetailscampaign',
            name='first_page_pre_text',
        ),
        migrations.AlterField(
            model_name='campaignfield',
            name='display_order',
            field=models.IntegerField(default=members.models.next_campaign_field_display_order),
        ),
        migrations.AlterField(
            model_name='profilefield',
            name='display_order',
            field=models.IntegerField(default=members.models.next_profile_field_display_order),
        ),
        migrations.DeleteModel(
            name='CampaignTag',
        ),
    ]
