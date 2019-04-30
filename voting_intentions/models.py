from django.db import models
from django.contrib.postgres.fields.citext import CIEmailField

# a vote for which intentions are being recorded
class Vote(models.Model):
    name = models.CharField(max_length = 100)
    redirect_url = models.CharField(max_length = 100, help_text = 'Redirects here after voting (unless a choice-level redirect is set)')
    
    def __str__(self):
        return self.name


# the URL parameters to pass on when redirecting
class UrlParameter(models.Model):
    vote = models.ForeignKey(Vote, related_name='url_parameters')
    name = models.CharField(max_length = 100, help_text = 'The name of the URL parameter to pass on when redirecting')
    pass_on_name = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'Set this to pass the parameter on with a different name')
    nation_builder_value = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'The value for this parameter in the NationBuilder URL above')
    
    def __str__(self):
        return self.name

# the possible voting intentions
class Choice(models.Model):
    vote = models.ForeignKey(Vote, related_name='choices')
    number = models.IntegerField(default = 0)
    text = models.CharField(max_length = 100)
    redirect_url = models.CharField(max_length = 100, blank=True, null=True, default=None, help_text = 'Set this to override the redirect for this choice')
    
    def __str__(self):
        return '%d - %s' % (self.number, self.text)

# NationBuilder tags that are set for a vote
class VoteTag(models.Model):
    vote = models.ForeignKey(Vote, related_name='vote_tags')
    text = models.CharField(max_length = 100, help_text = 'The tag to add to NationBuilder for this vote')
    add = models.BooleanField(default = True, help_text = 'Clear this to remove the tag instead')
    
    def __str__(self):
        return self.text

# NationBuilder tags that are set for a choice
class ChoiceTag(models.Model):
    choice = models.ForeignKey(Choice, related_name='choice_tags')
    text = models.CharField(max_length = 100, help_text = 'The tag to add to NationBuilder for this choice')
    add = models.BooleanField(default = True, help_text = 'Clear this to remove the tag instead')
    
    def __str__(self):
        return self.text

# a voting intention (associated with an email for now, eventually with a NationBuilder Id)
class Intention(models.Model):
    vote = models.ForeignKey(Vote, related_name='intentions')
    choice = models.ForeignKey(Choice, related_name='intentions')
    email = CIEmailField(verbose_name='email address', max_length=255)
    nation_builder_id = models.IntegerField(blank=True, null=True, default=None)
    recorded_at = models.DateTimeField(auto_now_add=True)
    tags_written_to_nation_builder = models.BooleanField(default=False)
    email_unknown_in_nation_builder = models.NullBooleanField(default=None)
    processed_at = models.DateTimeField(blank=True, null=True, default=None)
    
    def __str__(self):
        return self.email
