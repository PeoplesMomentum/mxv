from django.db import models
from django.contrib.postgres.fields.citext import CIEmailField

# a vote for which intentions are being recorded
class Vote(models.Model):
    name = models.TextField()
    redirect_url = models.TextField()
    
    def __str__(self):
        return self.name


# the URL parameters to pass on when redirecting
class UrlParameter(models.Model):
    vote = models.ForeignKey(Vote, related_name='url_parameters')
    name = models.TextField()
    pass_on_name = models.TextField(default = '')
    
    def __str__(self):
        return self.name

# the possible voting intentions
class Choice(models.Model):
    vote = models.ForeignKey(Vote, related_name='choices')
    text = models.TextField()
    redirect_url = models.TextField(default = '')
    
    def __str__(self):
        return self.text

# NationBuilder tags that are set for a vote
class VoteTag(models.Model):
    vote = models.ForeignKey(Vote, related_name='vote_tags')
    text = models.TextField()
    add = models.BooleanField(default = True)
    
    def __str__(self):
        return self.text

# NationBuilder tags that are set for a choice
class ChoiceTag(models.Model):
    choice = models.ForeignKey(Choice, related_name='choice_tags')
    text = models.TextField()
    add = models.BooleanField(default = True)
    
    def __str__(self):
        return self.text

# a voting intention (associated with an email for now, eventually with a NationBuilder Id)
class Intention(models.Model):
    vote = models.ForeignKey(Vote, related_name='intentions')
    choice = models.ForeignKey(Choice, related_name='intentions')
    email = CIEmailField(verbose_name='email address', max_length=255)
    nation_builder_id = models.IntegerField(blank=True, null=True, default=None)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
