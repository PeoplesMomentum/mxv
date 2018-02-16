from django.db import models
from mxv.settings import AUTH_USER_MODEL
from datetime import date
from django.core.mail.message import EmailMultiAlternatives
from django.urls.base import reverse
from django.utils import formats

# field sizes
name_length = 100
summary_length = 500
description_length = 1000
text_length = 4000

# a track in the democracy review
class Track(models.Model):
    # appearance
    name = models.CharField(max_length=name_length, unique=True)
    display_order = models.IntegerField(default = 1)
    description = models.TextField(max_length=description_length, default='')
    # visibility
    show_amendments = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)
    # permissions
    allow_submissions = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    allow_nominations = models.BooleanField(default=True)
    # submission dates
    submission_start = models.DateField(blank=True, null=True, default=None)
    submission_end = models.DateField(blank=True, null=True, default=None)
    # nomination dates
    nomination_start = models.DateField(blank=True, null=True, default=None)
    nomination_end = models.DateField(blank=True, null=True, default=None)
    
    def __str__(self):
        return self.name
    
    def submissions_in_range(self):
        today = date.today()
        return self.submission_start != None and self.submission_end != None and today >= self.submission_start and today <= self.submission_end
    
    def nominations_in_range(self):
        today = date.today()
        return self.nomination_start != None and self.nomination_end != None and today >= self.nomination_start and today <= self.nomination_end
    
    # whether submissions are allowed today
    def submissions_currently_allowed(self):
        return self.allow_submissions and self.submissions_in_range()

    # whether nominations are allowed today
    def nominations_currently_allowed(self):
        return self.allow_nominations and self.nominations_in_range()
    
    # description of submission dates
    def submission_date_text(self):
        if self.submissions_in_range():
            return '%s - %s' % (formats.date_format(self.submission_start, 'd/m/Y'), formats.date_format(self.submission_end, 'd/m/Y'))
        else:
            return 'Completed'
        
    # description of nomination dates
    def nomination_date_text(self):
        if self.nomination_start == None and self.nomination_end == None:
            return 'N/A'
        elif self.nominations_in_range():
            return '%s - %s' % (formats.date_format(self.nomination_start, 'd/m/Y'), formats.date_format(self.nomination_end, 'd/m/Y'))
        else:
            return 'Completed'
        
    # earliest track date
    def earliest(self):
        starts = []
        if self.allow_submissions:
            starts.append(self.submission_start)
        if self.allow_nominations:
            starts.append(self.nomination_start)
        if len(starts) == 0:
            return None
        else:
            return min(starts)

    # latest track date
    def latest(self):
        ends = []
        if self.allow_submissions:
            ends.append(self.submission_end)
        if self.allow_nominations:
            ends.append(self.nomination_end)
        if len(ends) == 0:
            return None
        else:
            return max(ends)
    
    # track guidance
    def guidance(self):
        today = date.today()
        if self.earliest() != None and self.latest() != None:
            if today < self.earliest():
                return 'This track will be opening for submissions on %s' % formats.date_format(self.earliest(), 'l jS F')
            elif today >= self.earliest() and today <= self.latest():
                return 'This track is now live - and closes at midnight on %s' % formats.date_format(self.latest(), 'l jS F')
        return 'The official deadline has passed, but Momentum members can still provide feedback on the proposals submitted.'
    
    # track guidance CSS
    def guidance_class(self):
        today = date.today()        
        if self.earliest() != None and self.latest() != None and today >= self.earliest() and today <= self.latest():
            return 'text-danger'
        else:
            return 'text-muted'
        
# a theme in a track
class Theme(models.Model):
    track = models.ForeignKey(Track, related_name='themes')    
    name = models.CharField(max_length=name_length, unique=True)
    description = models.TextField(max_length=description_length)
    display_order = models.IntegerField(default = 1)
    guidance = models.TextField(max_length=description_length, default = '')
    
    def __str__(self):
        return self.name

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
    
    def __str__(self):
        return self.text
    
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
    
    

