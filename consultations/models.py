from django.db import models
from mxv.settings import AUTH_USER_MODEL

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
        return self.template

# a question on a consultation
class Question(models.Model):
    consultation = models.ForeignKey(Consultation, related_name='questions')
    number = models.PositiveIntegerField()
    text = models.TextField(max_length=description_length)
    multipleAnswersAllowed = models.BooleanField()

    def __str__(self):
        return '%d - %s' % (self.number, self.text)

# a possible answer to a question
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    display_order = models.PositiveIntegerField(default=1)
    text = models.CharField(max_length=name_length)

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

