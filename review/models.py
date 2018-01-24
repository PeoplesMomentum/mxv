from django.db import models
from mxv.settings import AUTH_USER_MODEL
from django.utils.text import Truncator
from datetime import date

# field sizes
name_length = 100
description_length = 1000
text_length = 4000
short_length = 100

# a track in the democracy review
class Track(models.Model):
    # appearance
    name = models.CharField(max_length=name_length, unique=True)
    display_order = models.IntegerField(default = 1)
    urgent = models.BooleanField(default=False)
    # visibility
    show_amendments = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)
    # permissions
    allow_submissions = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    allow_nominations = models.BooleanField(default=True)
    # submissions
    submission_start = models.DateField(blank=True, null=True, default=None)
    submission_end = models.DateField(blank=True, null=True, default=None)
    # nomination dates
    nomination_start = models.DateField(blank=True, null=True, default=None)
    nomination_end = models.DateField(blank=True, null=True, default=None)
    
    def __str__(self):
        return self.name
    
    def submissions_currently_allowed(self):
        return self.allow_submissions and date.today() >= self.submission_start <= self.submission_end

    def nominations_currently_allowed(self):
        return self.allow_nominations and date.today() >= self.nomination_start <= self.nomination_end

# a theme in a track
class Theme(models.Model):
    track = models.ForeignKey(Track, related_name='themes')    
    name = models.CharField(max_length=name_length, unique=True)
    description = models.TextField(max_length=description_length)
    display_order = models.IntegerField(default = 1)
    guidance = models.TextField(max_length=description_length, default = '')
    
    def __str__(self):
        return self.name
    
    def short_description(self):
        return Truncator(self.description).chars(short_length, '...')

# proposal in a theme
class Proposal(models.Model):
    theme = models.ForeignKey(Theme, related_name='proposals')
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='proposals')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=name_length)
    text = models.TextField(max_length=text_length)
    
    def __str__(self):
        return self.name
    
    def short_text(self):
        return Truncator(self.text).chars(short_length, '...')
    
# previous versions of a proposal
class ProposalHistory(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='history')
    created_at = models.DateTimeField()    
    name = models.CharField(max_length=name_length)
    text = models.TextField(max_length=text_length)

# proposal URLs
class ProposalURL(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='urls')
    url = models.TextField(max_length=description_length)
    display_text = models.TextField(max_length=description_length)

# an amendment to a proposal
class Amendment(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='amendments')
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='amendments')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=name_length)
    text = models.TextField(max_length=text_length)
    
    def __str__(self):
        return self.name
    
    def short_text(self):
        return Truncator(self.text).chars(short_length, '...')

# previous versions of an amendment
class AmendmentHistory(models.Model):
    amendment = models.ForeignKey(Amendment, related_name='history')
    created_at = models.DateTimeField()    
    text = models.TextField(max_length=text_length)

# a comment on a proposal
class Comment(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='comments')
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=text_length)
    
    def short_text(self):
        return Truncator(self.text).chars(short_length, '...')

# a member's nomination of a proposal
class Nomination(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='nominations')
    nominated_by = models.ForeignKey(AUTH_USER_MODEL, related_name='nominations')
    nominated_at = models.DateTimeField(auto_now_add=True)
    
# a moderation request
class ModerationRequest(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='moderation_requests', blank=True, null=True, default=None)
    amendment = models.ForeignKey(Amendment, related_name='moderation_requests', blank=True, null=True, default=None)
    comment = models.ForeignKey(Comment, related_name='moderation_requests', blank=True, null=True, default=None)
    requested_by = models.ForeignKey(AUTH_USER_MODEL, related_name='moderation_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=text_length, default='')
    

