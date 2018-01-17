from django.db import models
from mxv.settings import AUTH_USER_MODEL
from django.utils.text import Truncator

# field sizes
name_length = 100
description_length = 1000
text_length = 4000

# a track in the democracy review
class Track(models.Model):
    name = models.CharField(max_length=name_length, unique=True)
    description = models.TextField(max_length=description_length)
    start = models.DateField()
    submission_deadline = models.DateField()
    nomination_deadline = models.DateField()
    display_order = models.IntegerField(default = 1)
    urgent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

# a theme in a track
class Theme(models.Model):
    track = models.ForeignKey(Track, related_name='themes')    
    name = models.CharField(max_length=name_length, unique=True)
    description = models.TextField(max_length=description_length)
    display_order = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.name
    
# proposal in a theme
class Proposal(models.Model):
    theme = models.ForeignKey(Theme, related_name='proposals')
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='proposals')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=name_length)
    text = models.TextField(max_length=text_length)
    views = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.name
    
    def short_text(self):
        return Truncator(self.text).chars(100, '...')
    
# previous versions of a proposal
class ProposalHistory(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='history')
    created_at = models.DateTimeField()    
    name = models.CharField(max_length=name_length)
    text = models.TextField(max_length=text_length)

# a member's nomination of a proposal
class Nomination(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='nominations')
    nominated_by = models.ForeignKey(AUTH_USER_MODEL, related_name='nominations')
    nominated_at = models.DateTimeField(auto_now_add=True)

# an amendment to a proposal
class Amendment(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='amendments')
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='amendments')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=name_length)
    text = models.TextField(max_length=text_length)

# previous versions of an amendment
class AmendmentHistory(models.Model):
    amendment = models.ForeignKey(Amendment, related_name='history')
    created_at = models.DateTimeField()    
    text = models.TextField(max_length=text_length)


