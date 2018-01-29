from django.db import models
from mxv.settings import AUTH_USER_MODEL
from django.utils.text import Truncator
from datetime import date
from django.core.mail.message import EmailMultiAlternatives
from django.urls.base import reverse

# field sizes
name_length = 100
summary_length = 500
description_length = 1000
text_length = 4000
short_length = 100

# a track in the democracy review
class Track(models.Model):
    # appearance
    name = models.CharField(max_length=name_length, unique=True)
    display_order = models.IntegerField(default = 1)
    urgent = models.BooleanField(default=False)
    description = models.TextField(max_length=description_length, default='')
    guidance = models.TextField(max_length=description_length, default='')
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
    summary = models.CharField(max_length=summary_length, default='')
    text = models.TextField(max_length=text_length)
    
    def __str__(self):
        return self.name
    
    def short_text(self):
        if self.summary != '':
            return Truncator(self.summary).chars(short_length, '...')
        else:
            return Truncator(self.text).chars(short_length, '...')
    
    def moderated(self):
        return self.moderation_requests.filter(moderated = True).exists()
    
# previous versions of a proposal
class ProposalHistory(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='history')
    created_at = models.DateTimeField()    
    name = models.CharField(max_length=name_length)
    summary = models.CharField(max_length=summary_length, default='')
    text = models.TextField(max_length=text_length)

# proposal URLs
class ProposalURL(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='urls')
    url = models.TextField(max_length=description_length)
    display_text = models.TextField(max_length=description_length)
    external = models.BooleanField(default=False)

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

    def moderated(self):
        return self.moderation_requests.filter(moderated = True).exists()
    
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

    def __str__(self):
        return self.short_text()
    
    def moderated(self):
        return self.moderation_requests.filter(moderated = True).exists()
    
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
    moderated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.reason
    
    def notify_staff(self, request):
        # build the email body
        entity = ''
        href = request.build_absolute_uri(reverse('admin:review_moderationrequest_change', args = (self.id,)))
        if self.proposal:
            entity = 'a proposal'
        elif self.amendment:
            entity = 'an amendment'
        elif self.comment:
            entity = 'a comment'
        body = 'Moderation of %s has been requested by %s (%s):\n\n  %s' % (
            entity, self.requested_by.name, self.requested_by.email, href)
        
        # send the email
        message = EmailMultiAlternatives(
            subject = 'Moderation required', 
            body = body,
            to = { notification.email_address for notification in ModerationRequestNotification.objects.all() }) 
        message.send()
            
    def moderated_entity_created_by(self):
        if self.proposal:
            return self.proposal.created_by
        elif self.amendment:
            return self.amendment.created_by
        elif self.comment:
            return self.comment.created_by
        else:
            return ''
    
# email addresses to notify about moderation requests
class ModerationRequestNotification(models.Model):
    email_address = models.EmailField(default = '')
    
    def __str__(self):
        return self.email_address
    
    

