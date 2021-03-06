# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-22 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_updatedetailscampaign'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignField',
            fields=[
                ('profilefield_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='members.ProfileField')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='members.UpdateDetailsCampaign')),
            ],
            bases=('members.profilefield',),
        ),
        migrations.CreateModel(
            name='CampaignTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='members.UpdateDetailsCampaign')),
            ],
        ),
    ]
