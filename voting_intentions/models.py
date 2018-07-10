from django.db import models
from django.contrib.postgres.fields.citext import CIEmailField

# a vote for which intentions are being recorded
class Vote(models.Model):
    name = models.TextField()
    redirect_url = models.TextField()

# the URL parameters to pass on when redirecting
class UrlParameter(models.Model):
    vote = models.ForeignKey(Vote, related_name='url_parameters')
    name = models.TextField()

# the possible voting intentions
class Choice(models.Model):
    vote = models.ForeignKey(Vote, related_name='choices')
    text = models.TextField()

# a voting intention (associated with an email for now, eventually with a NationBuilder Id)
class Intention(models.Model):
    vote = models.ForeignKey(Vote, related_name='intentions')
    choice = models.ForeignKey(Choice, related_name='intentions')
    email = CIEmailField(verbose_name='email address', max_length=255)
    recorded_at = models.DateTimeField(auto_now_add=True)
