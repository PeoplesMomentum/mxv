# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-29 08:10
from __future__ import unicode_literals

from django.db import migrations

# populates choice numbers from one in each vote
def populate_choice_numbers(apps, schema_editor):
    
    # get the vote model
    Vote = apps.get_model('voting_intentions', 'Vote')
    
    # set each vote's choices' numbers to ascending integers within each vote
    for vote in Vote.objects.all():
        number = 1
        for choice in vote.choices.order_by('id'):
            choice.number = number
            choice.save()
            number += 1

class Migration(migrations.Migration):
    
    dependencies = [
        ('voting_intentions', '0013_choice_number'),
    ]

    operations = [
        migrations.RunPython(populate_choice_numbers),
    ]