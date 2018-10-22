from django.db import models
from mxv.settings import AUTH_USER_MODEL
from datetime import date
from django.utils import formats

# field sizes
name_length = 255
description_length = 1000

# a consultation
class Consultation(models.Model):
    template = models.CharField(max_length=name_length)
    name = models.CharField(max_length=name_length, unique=True)
    description = models.TextField(max_length=description_length)
    voting_start = models.DateField()
    voting_end = models.DateField()

    def __str__(self):
        return self.name

    # whether voting is currently allowed
    def voting_in_range(self):
        today = date.today()
        return today >= self.voting_start and today <= self.voting_end
    
    # description of voting dates
    def voting_date_text(self):
        if self.voting_end > date.today():
            return '%s - %s' % (formats.date_format(self.voting_start, 'd/m/Y'), formats.date_format(self.voting_end, 'd/m/Y'))
        else:
            return 'Completed'
        
    # voting guidance
    def guidance(self):
        today = date.today()
        if today < self.voting_start:
            return 'Voting on this consultation will be starting on %s.' % formats.date_format(self.voting_start, 'l jS F')
        elif self.voting_in_range():
            return 'Voting on this consultation is now live - and closes at midnight on %s.' % formats.date_format(self.voting_end, 'l jS F')
        else:
            return 'Voting on this consultation has ended.'
    
    # voting guidance CSS
    def guidance_class(self):
        if self.voting_in_range():
            return 'text-danger'
        else:
            return 'text-muted'
        
    # voting button
    def vote_button_text(self):
        today = date.today()
        if today < self.voting_start:
            return 'View questions'
        elif self.voting_in_range():
            return 'Vote now'
        else:
            return 'View results'
    
# a question on a consultation
class Question(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='questions')
    number = models.PositiveIntegerField()
    text = models.TextField(max_length=description_length)
    guidance = models.TextField(max_length=description_length, default='')
    multipleAnswersAllowed = models.BooleanField()

    def __str__(self):
        return '%d - %s' % (self.number, self.text)

# a possible answer to a question
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    display_order = models.PositiveIntegerField(default=1)
    text = models.CharField(max_length=name_length)
    redirect_url = models.TextField(default='')

    def __str__(self):
        return self.text

class Vote(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='votes')
    member = models.ForeignKey(AUTH_USER_MODEL, related_name='consultation_votes')

    def __str__(self):
        return '%s / %s' % (self.consultation, self.member)
    
# a member's answer to a question
class Answer(models.Model):
    vote = models.ForeignKey(Vote, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')
    choice = models.ForeignKey(Choice, related_name='answers')
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s / %s' % (self.question, self.choice)

